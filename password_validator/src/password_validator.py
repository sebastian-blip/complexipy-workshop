"""
Password Validator - Simple example for refactoring demonstration
This module validates passwords based on security rules.
"""

import re


def validate_password(password, options=None):
    """
    Validate a password based on security rules.

    Args:
        password: The password to validate
        options: Optional configuration (min_length, require_special, etc.)

    Returns:
        dict: Validation result with success status and messages
    """
    if not password:
        return {
            "valid": False,
            "message": "Password is required",
            "errors": ["Password cannot be empty"],
        }

    # Default options
    if options is None:
        options = {}

    min_length = options.get("min_length", 8)
    max_length = options.get("max_length", 128)
    require_uppercase = options.get("require_uppercase", True)
    require_lowercase = options.get("require_lowercase", True)
    require_digits = options.get("require_digits", True)
    require_special = options.get("require_special", True)
    forbidden_words = options.get(
        "forbidden_words", ["password", "123456", "qwerty"]
    )

    errors = []
    warnings = []

    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters long")
    elif len(password) > max_length:
        errors.append(
            f"Password must be no more than {max_length} characters long"
        )

    if require_uppercase:
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")

    if require_lowercase:
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")

    if require_digits:
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")

    if require_special:
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            errors.append(
                "Password must contain at least one special character"
            )

    password_lower = password.lower()
    for word in forbidden_words:
        if word.lower() in password_lower:
            errors.append(f"Password cannot contain '{word}'")

    if re.search(r"(.)\1{2,}", password):
        warnings.append("Password contains repeated characters")

    if re.search(r"(012|123|234|345|456|567|678|789|890)", password):
        warnings.append("Password contains sequential numbers")

    if re.search(
        r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)",
        password.lower(),
    ):
        warnings.append("Password contains sequential letters")

    strength_score = 0

    if len(password) >= 8:
        strength_score += 2  # Base security requirement
    if len(password) >= 12:
        strength_score += 1  # Good length
    if len(password) >= 16:
        strength_score += 1  # Very good length
    if len(password) >= 20:
        strength_score += 1  # Excellent length

    if any(c.isupper() for c in password):
        strength_score += 1
    if any(c.islower() for c in password):
        strength_score += 1
    if any(c.isdigit() for c in password):
        strength_score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        strength_score += 1

    if strength_score <= 4:
        strength = "Weak"
    elif strength_score <= 6:
        strength = "Medium"
    elif strength_score <= 8:
        strength = "Strong"
    else:
        strength = "Very Strong"

    if len(password) >= 20:
        warnings.append(
            "Very long password - consider using a password manager"
        )

    keyboard_rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]
    for row in keyboard_rows:
        for i in range(len(row) - 2):
            pattern = row[i : i + 3]
            if pattern in password.lower():
                warnings.append(
                    f"Password contains keyboard pattern '{pattern}'"
                )

    is_valid = len(errors) == 0

    if is_valid:
        if len(warnings) == 0:
            message = f"Password is valid and {strength.lower()}"
        else:
            message = f"Password is valid but {strength.lower()} with {len(warnings)} warning(s)"
    else:
        message = f"Password is invalid with {len(errors)} error(s)"

    return {
        "valid": is_valid,
        "message": message,
        "errors": errors,
        "warnings": warnings,
        "strength": strength,
        "strength_score": strength_score,
    }


if __name__ == "__main__":
    test_passwords = [
        "weak",
        "Password123",
        "MySecure123!",
        "VerySecurePassword2024!@#",
        "qwerty123",
        "abc123ABC!",
    ]

    print("🔒 Password Validation Examples\n")

    for password in test_passwords:
        result = validate_password(password)
        print(f"Password: '{password}'")
        print(f"Result: {result['message']}")
        print(f"Strength: {result['strength']}")

        if result["errors"]:
            print("Errors:")
            for error in result["errors"]:
                print(f"  ❌ {error}")

        if result["warnings"]:
            print("Warnings:")
            for warning in result["warnings"]:
                print(f"  ⚠️  {warning}")

        print("-" * 50)

    print("\n📋 Custom Validation Rules\n")

    custom_options = {
        "min_length": 12,
        "require_special": False,
        "forbidden_words": ["admin", "user", "test"],
    }

    password = "AdminPassword123"

    result = validate_password(password, custom_options)
    print(f"Password: {password}")
    print(f"Custom rules result: {result['message']}")

    if result["errors"]:
        for error in result["errors"]:
            print(f"  ❌ {error}")
