from live_demo.src.live_refactor_example import (
    validate_user_registration,
)


def test_valid_registration():
    """Test valid user registration."""
    result = validate_user_registration(
        "john@example.com", "Password123!", "John Doe"
    )
    assert result["success"] is True
    assert result["valid"] is True


def test_invalid_email():
    """Test invalid email."""
    result = validate_user_registration("bad-email", "Password123!", "John Doe")
    assert result["success"] is False
    assert "Email" in str(result["errors"])


def test_weak_password():
    """Test weak password."""
    result = validate_user_registration("john@example.com", "weak", "John Doe")
    assert result["success"] is False
    assert any("Password" in error for error in result["errors"])


def test_empty_fields():
    """Test empty fields."""
    result = validate_user_registration("", "", "")
    assert result["success"] is False
    assert len(result["errors"]) >= 3
