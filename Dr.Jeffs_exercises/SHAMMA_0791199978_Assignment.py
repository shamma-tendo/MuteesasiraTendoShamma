"""
MUTEESASIRA TENDO SHAMMA_0791199978_assignment.py
─────────────────────────────────────────────────────────────
Contact Management System
  • Task 1 – Data Validation      (phone & email rules)
  • Task 2 – Advanced Search      (name / phone / email + pretty table)
  • Task 3 – Interactive CLI Menu (main() loop)

HOW TO REUSE IN ANOTHER SCRIPT
  from student_contact_assignment import ContactManager
  cm = ContactManager("my_contacts.db")
  cm.add_contact("Alice", "+256-701-111111", "alice@example.com")
  cm.list_all_contacts()
  cm.close()
─────────────────────────────────────────────────────────────────────
"""


import sqlite3   
import re        


# ══════════════════════════════════════════════════════════════════════════════
#  CLASS: ContactManager
#  ─────────────────────────────────────────────────────────────────────────────
#  All contact operations live inside this class so the logic is grouped in
#  one place and easy to import or extend later.
#
#  PRIVATE methods (names start with _) are internal helpers.
#  PUBLIC methods (no leading _) are the ones you call from outside the class.
# ══════════════════════════════════════════════════════════════════════════════

class ContactManager:
    """
    Manages a persistent SQLite contact database.
    Supports Create, Read, Update, Delete, and Search operations.
    """

    # ── Constructor ────────────────────────────────────────────────────────────

    def __init__(self, db_name: str = "contacts.db"):
        """
        Called automatically when you write: manager = ContactManager()

        db_name  – name of the SQLite file to open (or create).
                   Pass ":memory:" in tests to use a temporary in-memory DB
                   that leaves no file on disk.
        """
        # Open a connection to the database file.
        # If the file does not exist yet, SQLite creates it automatically.
        self.conn = sqlite3.connect(db_name)

       
        self.cursor = self.conn.cursor()

        # Make sure the contacts table exists before any other method runs.
        self._create_table()

    # ── Database schema ────────────────────────────────────────────────────────

    def _create_table(self):
        """
        Creates the 'contacts' table the very first time the program runs.
        On subsequent runs the IF NOT EXISTS clause makes this a safe no-op
        (it does nothing if the table is already there).

        Table columns:
          id    – auto-incrementing integer; uniquely identifies every contact.
          name  – required text field; may not be left empty (NOT NULL).
          phone – required text field; may not be left empty (NOT NULL).
          email – optional text field; defaults to an empty string ''.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT    NOT NULL,
                phone TEXT    NOT NULL,
                email TEXT    DEFAULT ''
            )
        """)
        # Write the schema change to disk immediately.
        self.conn.commit()


    # ══════════════════════════════════════════════════════════════════════════
    #  TASK 1 – VALIDATION HELPERS
    #  ─────────────────────────────────────────────────────────────────────────
    #  Both methods are @staticmethod because they don't need access to 'self'
    #  (no database reads/writes, no instance data).  They are pure input checks.
    #  You can call them without an instance: ContactManager._is_valid_phone(p)
    # ══════════════════════════════════════════════════════════════════════════

    @staticmethod
    def _is_valid_phone(phone: str) -> bool:
        """
        Returns True if the phone number contains ONLY:
          • an optional leading '+' (for international prefix, e.g. +256)
          • digits  0-9
          • hyphens  -

        Returns False if any other character is found (letters, spaces, etc.).

        REGEX BREAKDOWN  r'[+\\d][\\d\\-]*'
          [+\\d]   – first character must be '+' or a digit (mandatory)
          [\\d\\-]* – zero or more digits or hyphens after that

        re.fullmatch() ensures the pattern covers the ENTIRE string, not just
        a part of it (unlike re.match which only checks from the start).

        Examples that PASS : +256-701-123456  |  0772123456  |  1-800-555-0199
        Examples that FAIL : abc123  |  +256 701  |  07!1234
        """
        return bool(re.fullmatch(r'[+\d][\d\-]*', phone))

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        Returns True when:
          1. The email field is empty (email is optional for a contact), OR
          2. The string contains '@' AND the part after '@' contains a dot '.'.

        Checking the dot in the DOMAIN part (after '@') catches addresses like
        'user@' or 'not.valid@' that would slip through a simpler check.

        HOW IT WORKS
          email.split("@") splits "alice@mail.com" into ["alice", "mail.com"].
          We then check whether "." appears in "mail.com" (index [1]).

        Examples that PASS : alice@mail.com  |  a.b@x.co.ug  |  "" (empty)
        Examples that FAIL : noatsymbol.com  |  nodot@nodot  |  dot.before@
        """
        if email:                           # Only validate if something was typed.
            if "@" not in email:
                return False                # Must have an @ symbol.
            domain = email.split("@")[1]    # Isolate everything after the @.
            return "." in domain            # Domain must contain at least one dot.
        return True                         # Empty email is always acceptable.


    # ══════════════════════════════════════════════════════════════════════════
    #  CRUD OPERATIONS
    #  Create → add_contact
    #  Read   → view_contact
    #  Update → update_contact
    #  Delete → delete_contact
    # ══════════════════════════════════════════════════════════════════════════

    def add_contact(self, name: str, phone: str, email: str = "") -> None:
        """
        Adds a new contact to the database after three checks:
          1. Phone format is valid.
          2. Email format is valid (if one was provided).
          3. No contact with the same name already exists (case-insensitive).

        If any check fails, an error message is printed and the method returns
        early — the database is never touched.

        Parameters
        ----------
        name  : Full name of the contact (required).
        phone : Phone number string (required).
        email : Email address (optional; defaults to empty string).
        """

        # ── Check 1: phone format ──────────────────────────────────────────────
        if not self._is_valid_phone(phone):
            # Print a helpful message and stop.  Do NOT insert anything.
            print(
                f"\n  [ERROR] Invalid phone number '{phone}'.\n"
                "          Use only digits and hyphens, e.g. +256-701-123456."
            )
            return   # Exit the method immediately; nothing is saved.

        # ── Check 2: email format ──────────────────────────────────────────────
        if not self._is_valid_email(email):
            print(
                f"\n  [ERROR] Invalid email '{email}'.\n"
                "          Email must contain '@' and a '.' after it."
            )
            return   # Exit the method immediately; nothing is saved.

        # ── Check 3: duplicate name ────────────────────────────────────────────
        # LOWER() makes the comparison case-insensitive so "Alice" and "alice"
        # are treated as the same name.
        self.cursor.execute(
            "SELECT id FROM contacts WHERE LOWER(name) = LOWER(?)",
            (name.strip(),),   # .strip() removes accidental leading/trailing spaces.
        )
        if self.cursor.fetchone():
            # fetchone() returns a row tuple if a match was found, or None if not.
            print(f"\n  [ERROR] A contact named '{name}' already exists.")
            return   # Exit the method; no duplicate is inserted.

        # ── All checks passed → insert the new row ─────────────────────────────
        # The '?' placeholders are filled by the tuple in the second argument.
        # This is called a parameterised query and it prevents SQL-injection attacks.
        self.cursor.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (name.strip(), phone.strip(), email.strip()),
        )
        self.conn.commit()   # Write the change to disk so it is not lost on exit.
        print(f"\n  [OK] Contact '{name}' added successfully.")

    # ──────────────────────────────────────────────────────────────────────────

    def view_contact(self, contact_id: int) -> None:
        """
        Looks up a single contact by its unique numeric ID and displays it.

        We use ID (not name) for lookup because two people can share a name,
        but every ID in the database is guaranteed to be unique.

        Parameters
        ----------
        contact_id : The integer ID shown in the 'ID' column of the table.
        """
        # SELECT the four columns we care about for the matching row.
        self.cursor.execute(
            "SELECT id, name, phone, email FROM contacts WHERE id = ?",
            (contact_id,),   # The trailing comma makes this a tuple (required by sqlite3).
        )
        row = self.cursor.fetchone()   # Returns one tuple, or None if no match.

        if row:
            # Contact found → display it in the formatted table.
            print(f"\n  Contact details for ID {contact_id}:")
            self._print_table_header()
            self._print_table_row(row)
            self._print_table_footer()
        else:
            # No contact with that ID exists in the database.
            print(f"\n  [INFO] No contact found with ID {contact_id}.")

    # ──────────────────────────────────────────────────────────────────────────

    def update_contact(
        self,
        contact_id: int,
        name:  str | None = None,   # Pass a string to change, or None to keep old value.
        phone: str | None = None,
        email: str | None = None,
    ) -> None:
        """
        Updates one or more fields of an existing contact.

        Only the fields you supply are changed; any field left as None keeps
        its current database value.  This makes partial updates easy:

          manager.update_contact(3, phone="0772-999999")  # only phone changes
          manager.update_contact(3, email="new@mail.com") # only email changes

        The new phone and email are validated before anything is written.

        Parameters
        ----------
        contact_id : ID of the contact to update.
        name       : New name, or None to keep the current name.
        phone      : New phone, or None to keep the current phone.
        email      : New email, or None to keep the current email.
        """

        # ── Step 1: check the contact actually exists ──────────────────────────
        self.cursor.execute(
            "SELECT id, name, phone, email FROM contacts WHERE id = ?",
            (contact_id,),
        )
        row = self.cursor.fetchone()

        if not row:
            print(f"\n  [INFO] No contact found with ID {contact_id}.")
            return   # Nothing to update; stop here.

        # Unpack the current row so we can use the existing values as fallbacks.
        _, cur_name, cur_phone, cur_email = row

        # ── Step 2: resolve final values ──────────────────────────────────────
        # If the caller passed a new value, use it.  Otherwise keep the old one.
        # .strip() removes any accidental surrounding whitespace from user input.
        new_name  = name.strip()  if name  is not None else cur_name
        new_phone = phone.strip() if phone is not None else cur_phone
        new_email = email.strip() if email is not None else cur_email

        # ── Step 3: validate the resolved values ──────────────────────────────
        # We validate the FINAL value (which might be unchanged) so the database
        # can never accidentally end up with invalid data from a previous entry.
        if not self._is_valid_phone(new_phone):
            print(
                f"\n  [ERROR] Invalid phone number '{new_phone}'.\n"
                "          Use only digits and hyphens, e.g. +256-701-123456."
            )
            return   # Stop; nothing is changed in the database.

        if not self._is_valid_email(new_email):
            print(
                f"\n  [ERROR] Invalid email '{new_email}'.\n"
                "          Email must contain '@' and a '.' after it."
            )
            return   # Stop; nothing is changed in the database.

        # ── Step 4: write the update to the database ───────────────────────────
        self.cursor.execute(
            "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
            (new_name, new_phone, new_email, contact_id),
        )
        self.conn.commit()   # Flush the change to the .db file on disk.
        print(f"\n  [OK] Contact ID {contact_id} updated successfully.")

    # ──────────────────────────────────────────────────────────────────────────

    def delete_contact(self, contact_id: int) -> None:
        """
        Permanently removes a contact from the database.

        We do a SELECT before the DELETE so we can:
          a) Confirm the contact exists and show a meaningful error if not.
          b) Report the contact's name in the success message.

        Parameters
        ----------
        contact_id : ID of the contact to delete.
        """

        # ── Step 1: confirm the contact exists and fetch its name ──────────────
        self.cursor.execute(
            "SELECT name FROM contacts WHERE id = ?", (contact_id,)
        )
        row = self.cursor.fetchone()

        if not row:
            print(f"\n  [INFO] No contact found with ID {contact_id}.")
            return   # Nothing to delete; stop here.

        # ── Step 2: delete the row ─────────────────────────────────────────────
        self.cursor.execute(
            "DELETE FROM contacts WHERE id = ?", (contact_id,)
        )
        self.conn.commit()   # Make the deletion permanent on disk.

        # row[0] is the name we fetched in Step 1, used in the confirmation message.
        print(f"\n  [OK] Contact '{row[0]}' (ID {contact_id}) deleted.")


    # ══════════════════════════════════════════════════════════════════════════
    #  TASK 2 – ADVANCED SEARCH
    #  ─────────────────────────────────────────────────────────────────────────
    #  The original brief asked for search by name and phone only.
    #  This implementation also searches by EMAIL using SQL's OR clause.
    #  Results are shown in a formatted table instead of a raw list of tuples.
    # ══════════════════════════════════════════════════════════════════════════

    def search_contacts(self, query: str) -> None:
       

        # Wrap the query in SQL wildcard characters for a partial match.
        # Example: query="alice" becomes pattern="%alice%"
        pattern = f"%{query}%"

        self.cursor.execute(
            """
            SELECT id, name, phone, email
            FROM   contacts
            WHERE  name  LIKE ?
               OR  phone LIKE ?
               OR  email LIKE ?
            ORDER  BY name
            """,
            # The same pattern is supplied three times, once for each LIKE clause.
            (pattern, pattern, pattern),
        )
        rows = self.cursor.fetchall()   # Returns a list of tuples, or [] if none found.

        print(f"\n  Search results for '{query}':")

        if rows:
            # Display each matching contact in the formatted table.
            self._print_table_header()
            for row in rows:
                self._print_table_row(row)
            self._print_table_footer()
            print(f"  {len(rows)} result(s) found.\n")
        else:
            print("  No contacts matched your search.\n")

    # ──────────────────────────────────────────────────────────────────────────

    def list_all_contacts(self) -> None:
        """
        Fetches every contact from the database and displays them in a table,
        sorted alphabetically by name (ORDER BY name).
        """
        self.cursor.execute(
            "SELECT id, name, phone, email FROM contacts ORDER BY name"
        )
        rows = self.cursor.fetchall()   # All rows as a list of tuples.

        print("\n  All Contacts:")

        if rows:
            self._print_table_header()
            for row in rows:           # Iterate and print one row at a time.
                self._print_table_row(row)
            self._print_table_footer()
            print(f"  Total: {len(rows)} contact(s).\n")
        else:
            # The table exists but has no rows yet.
            print("  No contacts saved yet.\n")


    # ══════════════════════════════════════════════════════════════════════════
    #  PRIVATE DISPLAY HELPERS
    #  ─────────────────────────────────────────────────────────────────────────
    #  These three methods work together to draw a bordered ASCII table:
    #
    #    _print_table_header()  →  top border + column titles + divider
    #    _print_table_row()     →  one data row per contact
    #    _print_table_footer()  →  closing border
    #
    #  They are private (leading _) because they are only used inside this class
    #  and are not part of the public API.
    # ══════════════════════════════════════════════════════════════════════════

    # Column widths in characters for: ID, Name, Phone, Email.
    # Change these numbers to widen/narrow any column globally.
    _COL_WIDTHS = (5, 22, 18, 28)

    def _print_table_header(self) -> None:
        """Prints the top border and the column-title row."""
        w = self._COL_WIDTHS

        # Build the separator line by joining dashes for each column width.
        # Each column gets (width + 2) dashes to account for the spaces around text.
        sep = "  +" + "+".join("─" * (n + 2) for n in w) + "+"
        print(sep)

        # Print column titles, each left-aligned (:<width>) inside its column.
        print(
            f"  | {'ID':<{w[0]}} | {'Name':<{w[1]}} "
            f"| {'Phone':<{w[2]}} | {'Email':<{w[3]}} |"
        )
        print(sep)   # Second separator acts as a divider under the titles.

    def _print_table_row(self, row: tuple) -> None:
        cid, name, phone, email = row   # Unpack the tuple into named variables.
        w = self._COL_WIDTHS

        # Show a dash for contacts that have no email rather than a blank cell.
        email_display = email if email else "—"

        # :<{w[n]} means: left-align the value and pad it to exactly w[n] characters.
        print(
            f"  | {cid:<{w[0]}} | {name:<{w[1]}} "
            f"| {phone:<{w[2]}} | {email_display:<{w[3]}} |"
        )

    def _print_table_footer(self) -> None:
        """Prints the closing border under the last row."""
        w = self._COL_WIDTHS
        print("  +" + "+".join("─" * (n + 2) for n in w) + "+")

    # ──────────────────────────────────────────────────────────────────────────

    def close(self) -> None:
        """
        Closes the SQLite database connection.

        Always call this when you are done, especially in scripts that are
        NOT using the 'with' statement.  Closing flushes any pending writes
        and releases the file lock on contacts.db.
        """
        self.conn.close()


# ══════════════════════════════════════════════════════════════════════════════
#  TASK 3 – INTERACTIVE CLI MENU
#  ─────────────────────────────────────────────────────────────────────────────
#  The three functions below are MODULE-LEVEL (not inside the class).
#  They handle all user interaction so the ContactManager class stays focused
#  purely on data logic.
#
#  _print_menu()  – draws the menu (private helper, not called from outside)
#  _get_int()     – safely reads an integer ID from the user
#  main()         – the main loop; entry point of the whole program
# ══════════════════════════════════════════════════════════════════════════════

def _print_menu() -> None:
    """
    Prints the numbered menu to the terminal.
    Called at the top of every loop iteration so the user always sees
    the options after each action.
    """
    print("\n" + "=" * 35)
    print("    === Contact Manager Menu ===")
    print("=" * 35)
    print("  1. Add Contact")
    print("  2. View Contact")
    print("  3. Update Contact")
    print("  4. Delete Contact")
    print("  5. Search Contacts")
    print("  6. List All Contacts")
    print("  7. Exit")
    print("=" * 35)


def _get_int(prompt: str) -> int | None:
    """
    Prompts the user for a numeric contact ID and returns it as an integer.
    Returns None (instead of crashing) if the user types something that is
    not a number, so the caller can handle it gracefully.

    Parameters
    ----------
    prompt : The message shown to the user, e.g. "Enter contact ID : "
    """
    raw = input(prompt).strip()   # Read input and remove surrounding whitespace.

    if raw.isdigit():             # isdigit() is True only for strings of pure digits.
        return int(raw)           # Convert the string "3" to the integer 3.

    # If the input was not a number, tell the user and return None.
    print("  [ERROR] Please enter a valid numeric ID.")
    return None


def main() -> None:
    """
    Program entry point.  Runs a continuous while-loop that shows the menu,
    reads the user's choice, and calls the correct ContactManager method.

    The loop only exits when the user chooses option 7 (Exit).
    The database connection is closed cleanly before the program ends.
    """

    # Create one ContactManager instance for the whole session.
    # This opens (or creates) contacts.db in the current directory.
    manager = ContactManager()
    print("\n  Welcome to the Contact Manager!")
    print("  Your contacts are saved automatically.")

    # ── Main application loop ──────────────────────────────────────────────────
    while True:
        _print_menu()                                          # Show the menu.
        choice = input("  Choose an option (1-7): ").strip()  # Read the user's pick.

        # ── Option 1: Add a new contact ────────────────────────────────────────
        if choice == "1":
            print("\n  ── Add Contact ──")
            name  = input("  Name            : ").strip()
            phone = input("  Phone           : ").strip()
            # Email is optional; the user can press Enter to skip it.
            email = input("  Email (optional): ").strip()

            # Guard against blank name or phone before calling the method.
            if not name or not phone:
                print("  [ERROR] Name and phone are required.")
            else:
                manager.add_contact(name, phone, email)

        # ── Option 2: View one contact by ID ───────────────────────────────────
        elif choice == "2":
            print("\n  ── View Contact ──")
            cid = _get_int("  Enter contact ID : ")
            if cid is not None:          # Only proceed if a valid integer was given.
                manager.view_contact(cid)

        # ── Option 3: Update an existing contact ───────────────────────────────
        elif choice == "3":
            print("\n  ── Update Contact ──")
            cid = _get_int("  Enter contact ID to update : ")
            if cid is not None:
                print("  (Press Enter to keep the current value)")
                # 'or None' converts an empty string "" to None so the method
                # knows to leave that field unchanged in the database.
                name  = input("  New name   : ").strip() or None
                phone = input("  New phone  : ").strip() or None
                email_raw = input("  New email  : ").strip()
                # For email we use a named variable first so the logic is clear:
                # if the user typed something use it, otherwise pass None (no change).
                email = email_raw if email_raw else None
                manager.update_contact(cid, name=name, phone=phone, email=email)

        # ── Option 4: Delete a contact ─────────────────────────────────────────
        elif choice == "4":
            print("\n  ── Delete Contact ──")
            cid = _get_int("  Enter contact ID to delete : ")
            if cid is not None:
                # Ask for confirmation before a permanent, irreversible delete.
                confirm = input(
                    f"  Delete contact ID {cid}? This cannot be undone. (yes/no): "
                ).strip().lower()

                if confirm == "yes":
                    manager.delete_contact(cid)
                else:
                    # Any answer other than "yes" cancels the operation safely.
                    print("  Deletion cancelled.")

        # ── Option 5: Search contacts ──────────────────────────────────────────
        elif choice == "5":
            print("\n  ── Search Contacts ──")
            query = input("  Enter name, phone, or email to search : ").strip()
            if query:
                manager.search_contacts(query)
            else:
                # An empty search would match every contact — prevent that.
                print("  [ERROR] Search query cannot be empty.")

        # ── Option 6: List all contacts ────────────────────────────────────────
        elif choice == "6":
            manager.list_all_contacts()

        # ── Option 7: Exit the program ─────────────────────────────────────────
        elif choice == "7":
            print("\n  Goodbye! Your contacts have been saved.\n")
            manager.close()   # Close the database connection cleanly before exit.
            break             # Exit the while-loop, ending the program.

        # ── Any other input is invalid ─────────────────────────────────────────
        else:
            print("  [ERROR] Invalid option. Please choose a number between 1 and 7.")


# ── Program entry point ────────────────────────────────────────────────────────
# This block runs only when the file is executed directly:
#   python student_contact_assignment.py
#
# It does NOT run when the file is imported as a module:
#   from student_contact_assignment import ContactManager
#
# This pattern lets the same file serve both as a runnable script and as an
# importable library without triggering the CLI loop on import.

if __name__ == "__main__":
    main()
