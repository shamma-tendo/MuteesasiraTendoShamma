"""
MUTEESASIRA TENDO SHAMMA_0791199978_assignment.py
─────────────────────────────────────────────────────────────
Contact Management System
  • Task 1 – Data Validation      (phone & email rules)
  • Task 2 – Advanced Search      (name / phone / email + pretty table)
  • Task 3 – Interactive CLI Menu (main() loop)
─────────────────────────────────────────────────────────────
"""

import sqlite3
import re



#  ContactManager Class

class ContactManager:
    """
    Manages a persistent SQLite contact database.
    Supports Create, Read, Update, Delete, and Search operations.
    """

    def __init__(self, db_name: str = "contacts.db"):
        """Open (or create) the database and ensure the table exists."""
        self.conn   = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    #  Schema 

    def _create_table(self):
        """Create the contacts table if it does not already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT    NOT NULL,
                phone TEXT    NOT NULL,
                email TEXT    DEFAULT ''
            )
        """)
        self.conn.commit()

    
    #  TASK 1 – Validation helpers
     

    @staticmethod
    def _is_valid_phone(phone: str) -> bool:
        """
        Phone must contain ONLY digits, hyphens, and an optional
        leading '+'.  Examples that pass: +256-701-123456, 0701123456
        """
        return bool(re.fullmatch(r'[+\d][\d\-]*', phone))

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        If an email is supplied it MUST contain '@' and '.'.
        An empty string (no email) is always accepted.
        """
        if email:                              # email is optional
            return "@" in email and "." in email
        return True

   
    #  Core CRUD Methods
    def add_contact(self, name: str, phone: str, email: str = "") -> None:
        """
        Insert a new contact after validating phone and email.
        Prints an error and cancels if validation fails.
        """
        #  Task 1 validation 
        if not self._is_valid_phone(phone):
            print(
                f"\n  [ERROR] Invalid phone number '{phone}'.\n"
                "          Use only digits and hyphens, e.g. +256-701-123456."
            )
            return

        if not self._is_valid_email(email):
            print(
                f"\n  [ERROR] Invalid email '{email}'.\n"
                "          Email must contain '@' and a '.' (period)."
            )
            return
        

        self.cursor.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (name.strip(), phone.strip(), email.strip()),
        )
        self.conn.commit()
        print(f"\n  [OK] Contact '{name}' added successfully.")


    def view_contact(self, contact_id: int) -> None:
        """Display a single contact by its numeric ID."""
        self.cursor.execute(
            "SELECT id, name, phone, email FROM contacts WHERE id = ?",
            (contact_id,),
        )
        row = self.cursor.fetchone()

        if row:
            print(f"\n  Contact details for ID {contact_id}:")
            self._print_table_header()
            self._print_table_row(row)
            self._print_table_footer()
        else:
            print(f"\n  [INFO] No contact found with ID {contact_id}.")



    def update_contact(
        self,
        contact_id: int,
        name:  str | None = None,
        phone: str | None = None,
        email: str | None = None,
    ) -> None:
        """
        Update one or more fields of an existing contact.
        Any argument left as None keeps the current value.
        Validates new phone/email before applying changes.
        """
        self.cursor.execute(
            "SELECT id, name, phone, email FROM contacts WHERE id = ?",
            (contact_id,),
        )
        row = self.cursor.fetchone()

        if not row:
            print(f"\n  [INFO] No contact found with ID {contact_id}.")
            return

        _, cur_name, cur_phone, cur_email = row

        # Resolve final values (keep current if nothing new supplied)
        new_name  = name.strip()  if name  is not None else cur_name
        new_phone = phone.strip() if phone is not None else cur_phone
        new_email = email.strip() if email is not None else cur_email

        #Task 1 validation 
        if not self._is_valid_phone(new_phone):
            print(
                f"\n  [ERROR] Invalid phone number '{new_phone}'.\n"
                "          Use only digits and hyphens, e.g. +256-701-123456."
            )
            return

        if not self._is_valid_email(new_email):
            print(
                f"\n  [ERROR] Invalid email '{new_email}'.\n"
                "          Email must contain '@' and a '.' (period)."
            )
            return
        

        self.cursor.execute(
            "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
            (new_name, new_phone, new_email, contact_id),
        )
        self.conn.commit()
        print(f"\n  [OK] Contact ID {contact_id} updated successfully.")

   

    def delete_contact(self, contact_id: int) -> None:
        """Remove a contact permanently by its ID."""
        self.cursor.execute(
            "SELECT name FROM contacts WHERE id = ?", (contact_id,)
        )
        row = self.cursor.fetchone()

        if not row:
            print(f"\n  [INFO] No contact found with ID {contact_id}.")
            return

        self.cursor.execute(
            "DELETE FROM contacts WHERE id = ?", (contact_id,)
        )
        self.conn.commit()
        print(f"\n  [OK] Contact '{row[0]}' (ID {contact_id}) deleted.")

  
    #  TASK 2 – Advanced Search
 

    def search_contacts(self, query: str) -> None:
        """
        Search across name, phone, AND email columns using a
        single query string (case-insensitive partial match).
        Results are displayed in a clean, formatted table rather
        than a raw list of tuples.
        """
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
            (pattern, pattern, pattern),
        )
        rows = self.cursor.fetchall()

        print(f"\n  Search results for '{query}':")

        if rows:
            self._print_table_header()
            for row in rows:
                self._print_table_row(row)
            self._print_table_footer()
            print(f"  {len(rows)} result(s) found.\n")
        else:
            print("  No contacts matched your search.\n")

    

    def list_all_contacts(self) -> None:
        """Display every contact sorted alphabetically by name."""
        self.cursor.execute(
            "SELECT id, name, phone, email FROM contacts ORDER BY name"
        )
        rows = self.cursor.fetchall()

        print("\n  All Contacts:")

        if rows:
            self._print_table_header()
            for row in rows:
                self._print_table_row(row)
            self._print_table_footer()
            print(f"  Total: {len(rows)} contact(s).\n")
        else:
            print("  No contacts saved yet.\n")

    
    #  Private display helpers (pretty-print table)
    

    _COL_WIDTHS = (5, 22, 18, 28)   # ID, Name, Phone, Email

    def _print_table_header(self) -> None:
        w = self._COL_WIDTHS
        sep = "  +" + "+".join("─" * (n + 2) for n in w) + "+"
        print(sep)
        print(
            f"  | {'ID':<{w[0]}} | {'Name':<{w[1]}} "
            f"| {'Phone':<{w[2]}} | {'Email':<{w[3]}} |"
        )
        print(sep)

    def _print_table_row(self, row: tuple) -> None:
        cid, name, phone, email = row
        w = self._COL_WIDTHS
        email_display = email if email else "—"
        print(
            f"  | {cid:<{w[0]}} | {name:<{w[1]}} "
            f"| {phone:<{w[2]}} | {email_display:<{w[3]}} |"
        )

    def _print_table_footer(self) -> None:
        w = self._COL_WIDTHS
        print("  +" + "+".join("─" * (n + 2) for n in w) + "+")

   

    def close(self) -> None:
        """Close the SQLite connection gracefully."""
        self.conn.close()



#  TASK 3 – Interactive CLI Menu


def _print_menu() -> None:
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
    """Prompt for an integer; return None if the user enters a non-number."""
    raw = input(prompt).strip()
    if raw.isdigit():
        return int(raw)
    print("  [ERROR] Please enter a valid numeric ID.")
    return None


def main() -> None:
    """
    Entry point: runs the interactive CLI loop until the user
    chooses option 7 (Exit).
    """
    manager = ContactManager()
    print("\n  Welcome to the Contact Manager!")
    print("  Your contacts are saved automatically.")

    while True:
        _print_menu()
        choice = input("  Choose an option (1-7): ").strip()

        # 1. Add Contact 
        if choice == "1":
            print("\n  ── Add Contact ──")
            name  = input("  Name           : ").strip()
            phone = input("  Phone          : ").strip()
            email = input("  Email (optional): ").strip()

            if not name or not phone:
                print("  [ERROR] Name and phone are required.")
            else:
                manager.add_contact(name, phone, email)

        # 2. View Contact 
        elif choice == "2":
            print("\n  ── View Contact ──")
            cid = _get_int("  Enter contact ID : ")
            if cid is not None:
                manager.view_contact(cid)

        # 3. Update Contact 
        elif choice == "3":
            print("\n  ── Update Contact ──")
            cid = _get_int("  Enter contact ID to update : ")
            if cid is not None:
                print("  (Press Enter to keep the current value)")
                name  = input("  New name   : ").strip() or None
                phone = input("  New phone  : ").strip() or None
                email_raw = input("  New email  : ").strip()
                # Pass None so the method knows NOT to wipe the stored email
                email = email_raw if email_raw else None
                manager.update_contact(cid, name=name, phone=phone, email=email)

        # 4. Delete Contact 
        elif choice == "4":
            print("\n  ── Delete Contact ──")
            cid = _get_int("  Enter contact ID to delete : ")
            if cid is not None:
                confirm = input(
                    f"  Delete contact ID {cid}? This cannot be undone. (yes/no): "
                ).strip().lower()
                if confirm == "yes":
                    manager.delete_contact(cid)
                else:
                    print("  Deletion cancelled.")

        # 5. Search Contacts 
        elif choice == "5":
            print("\n  ── Search Contacts ──")
            query = input("  Enter name, phone, or email to search : ").strip()
            if query:
                manager.search_contacts(query)
            else:
                print("  [ERROR] Search query cannot be empty.")

        # 6. List All Contacts
        elif choice == "6":
            manager.list_all_contacts()

        # 7. Exit 
        elif choice == "7":
            print("\n  Goodbye! Your contacts have been saved.\n")
            manager.close()
            break

        # Invalid option
        else:
            print("  [ERROR] Invalid option. Please choose a number between 1 and 7.")


#  Program entry point 
if __name__ == "__main__":
    main()
