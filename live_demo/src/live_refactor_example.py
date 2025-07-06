import re


def validate_user_registration(email, password, name):
    """
    Validate user registration data.
    """
    errors = []

    if not email:
        errors.append("Email is required")
    else:
        if len(email) < 5:
            errors.append("Email too short")
        if len(email) > 254:
            errors.append("Email too long")
        if "@" not in email:
            errors.append("Email must contain @")
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email
        ):
            errors.append("Email format invalid")

    if not password:
        errors.append("Password is required")
    else:
        if len(password) < 8:
            errors.append("Password too short")
        if len(password) > 128:
            errors.append("Password too long")
        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False
        for char in password:
            if char.isupper():
                has_upper = True
            if char.islower():
                has_lower = True
            if char.isdigit():
                has_digit = True
            if char in "!@#$%^&*":
                has_special = True
        if not has_upper:
            errors.append("Password needs uppercase")
        if not has_lower:
            errors.append("Password needs lowercase")
        if not has_digit:
            errors.append("Password needs digit")
        if not has_special:
            errors.append("Password needs special character")

    if not name:
        errors.append("Name is required")
    else:
        if len(name) < 2:
            errors.append("Name too short")
        if len(name) > 50:
            errors.append("Name too long")
        if not name.replace(" ", "").isalpha():
            errors.append("Name contains invalid characters")

    if errors:
        return {"success": False, "errors": errors, "valid": False}
    else:
        return {
            "success": True,
            "message": "Registration valid!",
            "valid": True,
        }


if __name__ == "__main__":
    test_cases = [
        ("john@example.com", "Password123!", "John Doe"),
        ("bad-email", "weak", "X"),
        ("", "", ""),
        ("good@email.com", "StrongPass1!", "Jane Smith"),
    ]

    for email, password, name in test_cases:
        result = validate_user_registration(email, password, name)
        print(f"\nTesting: {email}, {password}, {name}")
        print(f"Result: {result}")
