# ============================================================
#  Exercise 3: Custom Exception – Ugandan Driving Age Check
#  Rule: A person must be 18 years or older to drive in Uganda
# ============================================================


# ── Step 1: Define the custom exception ─────────────────────
class UnderAgeToDriveError(Exception):
    """
    Raised when a person is too young to legally drive in Uganda.
    The legal minimum driving age in Uganda is 18 years.
    """
    pass


# ── Step 2: Function that enforces the rule ──────────────────
def check_driving_eligibility(name: str, age: int) -> None:
    """
    Check whether a person meets Uganda's minimum driving age.

    Parameters:
        name (str) : The person's name.
        age  (int) : The person's age in years.

    Raises:
        UnderAgeToDriveError: If the person is younger than 18.
    """
    if age < 18:
        raise UnderAgeToDriveError(
            f"{name} is {age} years old and is NOT allowed to drive in Uganda. "
            "You must be 18 years or older."
        )
    print(f"✓ {name} is {age} years old and is eligible to drive in Uganda.")


# ── Step 3: Test with multiple people ───────────────────────
people = [
    ("Aisha Nakato",    16),   # too young
    ("Brian Otieno",    18),   # exactly the minimum – allowed
    ("Carol Namukasa",  25),   # well above minimum – allowed
    ("David Ssemakula", 12),   # too young
]

print("=" * 55)
print("   Uganda Driving Age Eligibility Checker")
print("=" * 55)

for name, age in people:
    try:
        check_driving_eligibility(name, age)

    except UnderAgeToDriveError as e:
        # Catch our custom exception and display a clear message
        print(f"✗ UnderAgeToDriveError: {e}")