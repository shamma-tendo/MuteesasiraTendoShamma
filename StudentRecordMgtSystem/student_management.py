"""
=============================================================
  Student Record Management System
  Author : Assignment Submission
  File   : student_management.py
  Purpose: Menu-driven app demonstrating file I/O, exception
           handling, logging, and data validation in Python.
=============================================================
"""

import csv
import json
import logging
import os
import re
from datetime import datetime

# ─────────────────────────────────────────────
#  File paths (all relative to the script dir)
# ─────────────────────────────────────────────
CSV_FILE  = "students.csv"
JSON_FILE = "students.json"
LOG_FILE  = "student_system.log"

# ─────────────────────────────────────────────
#  Logging configuration
#  Logs go to both the log file AND the console
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),          # persistent log
        logging.StreamHandler(),                 # live console output
    ],
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════
#  Custom Exceptions
# ═══════════════════════════════════════════════════════════

class StudentNotFoundError(Exception):
    """Raised when a registration number does not exist in the records."""
    pass


class DuplicateRegistrationError(Exception):
    """Raised when trying to add a student whose reg number already exists."""
    pass


class InvalidInputError(Exception):
    """Raised when user input fails validation checks."""
    pass


# ═══════════════════════════════════════════════════════════
#  Helper / Utility Functions
# ═══════════════════════════════════════════════════════════

def clear_screen():
    """Clear terminal screen for a cleaner UI experience."""
    os.system("cls" if os.name == "nt" else "clear")


def validate_reg_number(reg: str) -> str:
    """
    Validate registration number format: REG followed by 4 digits.
    Example valid formats: REG0001, REG1234
    Returns the upper-cased reg number or raises InvalidInputError.
    """
    reg = reg.strip().upper()
    pattern = r"^REG\d{4}$"
    if not re.match(pattern, reg):
        raise InvalidInputError(
            f"'{reg}' is not a valid registration number. "
            "Use format REG#### (e.g. REG0001)."
        )
    return reg


def validate_name(name: str) -> str:
    """Ensure name is non-empty and contains only alphabetic characters/spaces."""
    name = name.strip().title()
    if not name:
        raise InvalidInputError("Name cannot be empty.")
    if not re.match(r"^[A-Za-z\s\-']+$", name):
        raise InvalidInputError(
            "Name must contain only letters, spaces, hyphens, or apostrophes."
        )
    return name


def validate_year(year: str) -> int:
    """Ensure year of study is between 1 and 6 (inclusive)."""
    try:
        y = int(year.strip())
    except ValueError:
        raise InvalidInputError("Year of study must be a whole number.")
    if y < 1 or y > 6:
        raise InvalidInputError("Year of study must be between 1 and 6.")
    return y


def validate_gpa(gpa: str) -> float:
    """Ensure GPA is a float between 0.0 and 4.0."""
    try:
        g = float(gpa.strip())
    except ValueError:
        raise InvalidInputError("GPA must be a numeric value (e.g. 3.75).")
    if g < 0.0 or g > 4.0:
        raise InvalidInputError("GPA must be between 0.0 and 4.0.")
    return round(g, 2)


def validate_phone(phone: str) -> str:
    """Ensure phone contains only digits, spaces, dashes, or a leading +."""
    phone = phone.strip()
    if not re.match(r"^\+?[\d\s\-]{7,15}$", phone):
        raise InvalidInputError(
            "Phone number is invalid. Use digits, spaces, or dashes (7-15 chars)."
        )
    return phone


# ═══════════════════════════════════════════════════════════
#  CSV Functions  –  Core student fields
#  Fields stored: reg_number, name, year_of_study, gpa
# ═══════════════════════════════════════════════════════════

CSV_HEADERS = ["reg_number", "name", "year_of_study", "gpa"]


def _read_csv() -> list[dict]:
    """
    Read all records from the CSV file.
    Returns a list of dicts. Returns empty list if file doesn't exist.
    """
    if not os.path.exists(CSV_FILE):
        return []
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except (IOError, csv.Error) as e:
        logger.error("Failed to read CSV file: %s", e)
        raise


def _write_csv(records: list[dict]) -> None:
    """
    Overwrite the CSV file with the given list of records.
    Always writes headers first.
    """
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(records)
    except IOError as e:
        logger.error("Failed to write CSV file: %s", e)
        raise


def _find_csv_record(reg_number: str) -> dict | None:
    """Return the CSV record for reg_number, or None if not found."""
    for record in _read_csv():
        if record["reg_number"] == reg_number:
            return record
    return None


# ═══════════════════════════════════════════════════════════
#  JSON Functions  –  Extended student details
#  Fields stored: address, phone, email, program, enrolled_date
# ═══════════════════════════════════════════════════════════

def _read_json() -> dict:
    """
    Read the JSON details file.
    Returns a dict keyed by reg_number. Empty dict if file missing.
    """
    if not os.path.exists(JSON_FILE):
        return {}
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        logger.error("Failed to read JSON file: %s", e)
        raise


def _write_json(data: dict) -> None:
    """Overwrite the JSON file with the given dict."""
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        logger.error("Failed to write JSON file: %s", e)
        raise


# ═══════════════════════════════════════════════════════════
#  Core CRUD Operations
# ═══════════════════════════════════════════════════════════

def add_student() -> None:
    """
    Collect new student details from the user, validate all fields,
    then save basic info to CSV and extended info to JSON.
    Raises DuplicateRegistrationError if the reg number already exists.
    """
    print("\n─── Add New Student ───────────────────────────────")
    try:
        # ── Collect and validate each field ──
        reg_number = validate_reg_number(
            input("  Registration Number (e.g. REG0001) : ").strip()
        )

        # Check for duplicate BEFORE collecting more info
        if _find_csv_record(reg_number):
            raise DuplicateRegistrationError(
                f"A student with registration number {reg_number} already exists."
            )

        name       = validate_name(input("  Full Name                         : "))
        year       = validate_year(input("  Year of Study (1–6)               : "))
        gpa        = validate_gpa (input("  GPA (0.0 – 4.0)                   : "))
        program    = input("  Program / Course                  : ").strip()
        address    = input("  Address                           : ").strip()
        phone      = validate_phone(input("  Phone Number                      : "))
        email      = input("  Email Address                     : ").strip()

        # ── Write to CSV ──
        records = _read_csv()
        records.append({
            "reg_number"  : reg_number,
            "name"        : name,
            "year_of_study": str(year),
            "gpa"         : str(gpa),
        })
        _write_csv(records)

        # ── Write to JSON ──
        details = _read_json()
        details[reg_number] = {
            "program"      : program,
            "address"      : address,
            "phone"        : phone,
            "email"        : email,
            "enrolled_date": datetime.now().strftime("%Y-%m-%d"),
        }
        _write_json(details)

        logger.info("ACTION: Added student %s – %s", reg_number, name)
        print(f"\n  ✓ Student {name} ({reg_number}) added successfully.")

    except (DuplicateRegistrationError, InvalidInputError) as e:
        logger.warning("Add student failed: %s", e)
        print(f"\n  ✗ Error: {e}")
    except Exception as e:
        logger.error("Unexpected error while adding student: %s", e)
        print(f"\n  ✗ Unexpected error: {e}")
    finally:
        # 'finally' runs whether or not an exception occurred
        print("─" * 52)


def view_all_students() -> None:
    """
    Display all student records from the CSV file in a formatted table.
    """
    print("\n─── All Students ──────────────────────────────────")
    try:
        records = _read_csv()
        if not records:
            print("  No student records found.")
            logger.info("ACTION: Viewed all students – no records found.")
            return

        # Print table header
        print(f"  {'Reg No.':<10} {'Name':<25} {'Year':<6} {'GPA':<6}")
        print("  " + "─" * 50)

        for r in records:
            print(
                f"  {r['reg_number']:<10} "
                f"{r['name']:<25} "
                f"{r['year_of_study']:<6} "
                f"{r['gpa']:<6}"
            )

        logger.info("ACTION: Viewed all students – %d record(s) displayed.", len(records))

    except Exception as e:
        logger.error("Error viewing students: %s", e)
        print(f"\n  ✗ Could not retrieve records: {e}")
    finally:
        print("─" * 52)


def search_student() -> None:
    """
    Search for a specific student by registration number and
    display both CSV (basic) and JSON (extended) details.
    Raises StudentNotFoundError if no match is found.
    """
    print("\n─── Search Student ────────────────────────────────")
    try:
        reg_number = validate_reg_number(
            input("  Enter Registration Number : ").strip()
        )

        csv_record = _find_csv_record(reg_number)
        if not csv_record:
            raise StudentNotFoundError(
                f"No student with registration number {reg_number} was found."
            )

        details = _read_json().get(reg_number, {})

        # Display combined info
        print(f"\n  ┌─ Student Profile ─────────────────────────────")
        print(f"  │  Registration : {csv_record['reg_number']}")
        print(f"  │  Name         : {csv_record['name']}")
        print(f"  │  Year         : {csv_record['year_of_study']}")
        print(f"  │  GPA          : {csv_record['gpa']}")
        print(f"  │  Program      : {details.get('program', 'N/A')}")
        print(f"  │  Address      : {details.get('address', 'N/A')}")
        print(f"  │  Phone        : {details.get('phone', 'N/A')}")
        print(f"  │  Email        : {details.get('email', 'N/A')}")
        print(f"  │  Enrolled     : {details.get('enrolled_date', 'N/A')}")
        print(f"  └───────────────────────────────────────────────")

        logger.info("ACTION: Searched for student %s – found.", reg_number)

    except StudentNotFoundError as e:
        logger.warning("Search failed: %s", e)
        print(f"\n  ✗ {e}")
    except InvalidInputError as e:
        logger.warning("Search input invalid: %s", e)
        print(f"\n  ✗ Input error: {e}")
    except Exception as e:
        logger.error("Unexpected error during search: %s", e)
        print(f"\n  ✗ Unexpected error: {e}")
    finally:
        print("─" * 52)


def update_student() -> None:
    """
    Allow the user to update one or more fields for an existing student.
    Pressing Enter without typing skips a field (keeps the current value).
    """
    print("\n─── Update Student ────────────────────────────────")
    try:
        reg_number = validate_reg_number(
            input("  Enter Registration Number to update : ").strip()
        )

        csv_record = _find_csv_record(reg_number)
        if not csv_record:
            raise StudentNotFoundError(
                f"No student with registration number {reg_number} was found."
            )

        details = _read_json()
        json_record = details.get(reg_number, {})

        print(f"\n  Updating {csv_record['name']} ({reg_number})")
        print("  (Press Enter to keep the current value)\n")

        # ── Update CSV fields ──
        new_name = input(f"  Full Name [{csv_record['name']}] : ").strip()
        if new_name:
            csv_record["name"] = validate_name(new_name)

        new_year = input(f"  Year of Study [{csv_record['year_of_study']}] : ").strip()
        if new_year:
            csv_record["year_of_study"] = str(validate_year(new_year))

        new_gpa = input(f"  GPA [{csv_record['gpa']}] : ").strip()
        if new_gpa:
            csv_record["gpa"] = str(validate_gpa(new_gpa))

        # ── Update JSON fields ──
        new_program = input(f"  Program [{json_record.get('program', '')}] : ").strip()
        if new_program:
            json_record["program"] = new_program

        new_address = input(f"  Address [{json_record.get('address', '')}] : ").strip()
        if new_address:
            json_record["address"] = new_address

        new_phone = input(f"  Phone [{json_record.get('phone', '')}] : ").strip()
        if new_phone:
            json_record["phone"] = validate_phone(new_phone)

        new_email = input(f"  Email [{json_record.get('email', '')}] : ").strip()
        if new_email:
            json_record["email"] = new_email

        # ── Persist changes ──
        all_records = _read_csv()
        for i, r in enumerate(all_records):
            if r["reg_number"] == reg_number:
                all_records[i] = csv_record
                break
        _write_csv(all_records)

        details[reg_number] = json_record
        _write_json(details)

        logger.info("ACTION: Updated student %s.", reg_number)
        print(f"\n  ✓ Student {reg_number} updated successfully.")

    except StudentNotFoundError as e:
        logger.warning("Update failed – not found: %s", e)
        print(f"\n  ✗ {e}")
    except InvalidInputError as e:
        logger.warning("Update failed – invalid input: %s", e)
        print(f"\n  ✗ Input error: {e}")
    except Exception as e:
        logger.error("Unexpected error during update: %s", e)
        print(f"\n  ✗ Unexpected error: {e}")
    finally:
        print("─" * 52)


def delete_student() -> None:
    """
    Remove a student's records from both the CSV and JSON files
    after confirming with the user.
    Raises StudentNotFoundError if no match is found.
    """
    print("\n─── Delete Student ────────────────────────────────")
    try:
        reg_number = validate_reg_number(
            input("  Enter Registration Number to delete : ").strip()
        )

        csv_record = _find_csv_record(reg_number)
        if not csv_record:
            raise StudentNotFoundError(
                f"No student with registration number {reg_number} was found."
            )

        # Confirm deletion
        confirm = input(
            f"\n  Are you sure you want to delete {csv_record['name']} "
            f"({reg_number})? [yes/no] : "
        ).strip().lower()

        if confirm != "yes":
            print("  Deletion cancelled.")
            logger.info("ACTION: Deletion of %s cancelled by user.", reg_number)
            return

        # ── Remove from CSV ──
        all_records = _read_csv()
        updated = [r for r in all_records if r["reg_number"] != reg_number]
        _write_csv(updated)

        # ── Remove from JSON ──
        details = _read_json()
        details.pop(reg_number, None)   # safe pop (no error if key missing)
        _write_json(details)

        logger.info("ACTION: Deleted student %s – %s.", reg_number, csv_record["name"])
        print(f"\n  ✓ Student {reg_number} deleted successfully.")

    except StudentNotFoundError as e:
        logger.warning("Delete failed – not found: %s", e)
        print(f"\n  ✗ {e}")
    except InvalidInputError as e:
        logger.warning("Delete failed – invalid input: %s", e)
        print(f"\n  ✗ Input error: {e}")
    except Exception as e:
        logger.error("Unexpected error during deletion: %s", e)
        print(f"\n  ✗ Unexpected error: {e}")
    finally:
        print("─" * 52)


# ═══════════════════════════════════════════════════════════
#  Main Menu
# ═══════════════════════════════════════════════════════════

MENU = """
╔══════════════════════════════════════════╗
║     STUDENT RECORD MANAGEMENT SYSTEM     ║
╠══════════════════════════════════════════╣
║  1. Add a New Student                    ║
║  2. View All Students                    ║
║  3. Search Student by Reg Number         ║
║  4. Update Student Details               ║
║  5. Delete a Student Record              ║
║  0. Exit                                 ║
╚══════════════════════════════════════════╝
"""

ACTIONS = {
    "1": add_student,
    "2": view_all_students,
    "3": search_student,
    "4": update_student,
    "5": delete_student,
}


def main() -> None:
    """Entry point – display menu and dispatch to the correct function."""
    logger.info("═══ Student Record Management System Started ═══")

    while True:
        print(MENU)
        choice = input("  Enter your choice (0–5) : ").strip()

        if choice == "0":
            logger.info("═══ System exited by user. ═══")
            print("\n  Goodbye! Exiting the system.\n")
            break
        elif choice in ACTIONS:
            ACTIONS[choice]()
        else:
            print("\n  ✗ Invalid choice. Please enter a number between 0 and 5.\n")
            logger.warning("Invalid menu choice entered: '%s'", choice)

        input("\n  Press Enter to return to the menu...")
        clear_screen()


if __name__ == "__main__":
    main()
