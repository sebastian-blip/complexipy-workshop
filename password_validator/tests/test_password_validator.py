"""
Unit tests for password validator modules
"""

import unittest
from password_validator.src.password_validator import validate_password


class TestPasswordValidator(unittest.TestCase):
    """Test cases for original password validator"""

    def test_empty_password(self):
        """Test behavior with empty password"""
        result = validate_password("")
        self.assertFalse(result["valid"])
        self.assertIn("Password cannot be empty", result["errors"])

    def test_none_password(self):
        """Test behavior with None password"""
        result = validate_password(None)
        self.assertFalse(result["valid"])

    def test_valid_password(self):
        """Test with a valid password"""
        result = validate_password("MySecure123!")
        self.assertTrue(result["valid"])
        self.assertEqual(result["strength"], "Strong")

    def test_weak_password(self):
        """Test with a weak password"""
        result = validate_password("weak")
        self.assertFalse(result["valid"])
        self.assertEqual(result["strength"], "Weak")

    def test_password_too_short(self):
        """Test password length validation"""
        result = validate_password("Abc1!")
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("at least 8 characters" in error for error in result["errors"])
        )

    def test_missing_uppercase(self):
        """Test uppercase requirement"""
        result = validate_password("mypassword123!")
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("uppercase letter" in error for error in result["errors"])
        )

    def test_missing_lowercase(self):
        """Test lowercase requirement"""
        result = validate_password("MYPASSWORD123!")
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("lowercase letter" in error for error in result["errors"])
        )

    def test_missing_digits(self):
        """Test digit requirement"""
        result = validate_password("MyPassword!")
        self.assertFalse(result["valid"])
        self.assertTrue(any("digit" in error for error in result["errors"]))

    def test_missing_special_chars(self):
        """Test special character requirement"""
        result = validate_password("MyPassword123")
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("special character" in error for error in result["errors"])
        )

    def test_forbidden_words(self):
        """Test forbidden words detection"""
        result = validate_password("MyPassword123!")
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("password" in error.lower() for error in result["errors"])
        )

    def test_custom_options(self):
        """Test custom validation options"""
        options = {
            "min_length": 6,
            "require_special": False,
            "forbidden_words": ["admin"],
        }
        result = validate_password("Admin123", options)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("admin" in error.lower() for error in result["errors"])
        )

    def test_pattern_warnings(self):
        """Test pattern detection warnings"""
        result = validate_password("MyPassword123aaa!")
        # Should have warnings for repeated characters
        self.assertTrue(
            any("repeated" in warning for warning in result["warnings"])
        )

    def test_keyboard_patterns(self):
        """Test keyboard pattern detection"""
        result = validate_password("MyPassqwer123!")
        self.assertTrue(
            any("keyboard pattern" in warning for warning in result["warnings"])
        )

    def test_strength_calculation(self):
        """Test strength calculation"""
        weak_result = validate_password("Ab1!", {"min_length": 4})
        medium_result = validate_password("MyPass123!")
        strong_result = validate_password("MySecurePass123!")
        very_strong_result = validate_password("MyVerySecurePassword2024!")

        self.assertEqual(weak_result["strength"], "Weak")
        self.assertEqual(medium_result["strength"], "Medium")
        self.assertEqual(strong_result["strength"], "Strong")
        self.assertEqual(very_strong_result["strength"], "Very Strong")


class TestPasswordValidatorEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def test_very_long_password(self):
        """Test with very long password"""
        long_password = "A" * 150
        result = validate_password(long_password)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("no more than" in error for error in result["errors"])
        )

    def test_password_with_spaces(self):
        """Test password with spaces"""
        result = validate_password("My Secure 123!")
        self.assertTrue(result["valid"])

    def test_password_with_unicode(self):
        """Test password with unicode characters"""
        result = validate_password("MyPäss123!")
        self.assertTrue(result["valid"])

    def test_all_requirements_disabled(self):
        """Test with all requirements disabled"""
        options = {
            "min_length": 1,
            "require_uppercase": False,
            "require_lowercase": False,
            "require_digits": False,
            "require_special": False,
            "forbidden_words": [],
        }
        result = validate_password("a", options)
        self.assertTrue(result["valid"])

    def test_empty_forbidden_words(self):
        """Test with empty forbidden words list"""
        options = {"forbidden_words": []}
        result = validate_password("password123", options)
        self.assertFalse(result["valid"])
        self.assertFalse(
            any("cannot contain" in error for error in result["errors"])
        )

    def test_case_insensitive_forbidden_words(self):
        """Test case insensitive forbidden words"""
        options = {"forbidden_words": ["ADMIN"]}
        result = validate_password("MyAdmin123!", options)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("admin" in error.lower() for error in result["errors"])
        )


if __name__ == "__main__":
    unittest.main()
