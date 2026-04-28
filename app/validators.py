"""Validation helpers for password generation."""

import string


def validate_password_length(length: int) -> None:
    """Validate that the password length is at least four characters."""
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")


def validate_character_types(selected_types: list[str]) -> None:
    """Validate that at least one character type was selected."""
    if not selected_types:
        raise ValueError("Select at least one character type.")


def validate_password_options(length: int, groups: list[str]) -> None:
    """Validate password options before generating the password."""
    validate_password_length(length)
    validate_character_types(groups)

    if length < len(groups):
        raise ValueError(
            "Password length must be at least the number of selected groups."
        )


def is_password_valid(
    password: str,
    uppercase: bool,
    lowercase: bool,
    numbers: bool,
    symbols: bool,
) -> bool:
    """Return True when the password matches the selected rules."""
    rules = [
        (uppercase, string.ascii_uppercase),
        (lowercase, string.ascii_lowercase),
        (numbers, string.digits),
        (symbols, string.punctuation),
    ]

    return all(
        any(character in group for character in password)
        for enabled, group in rules
        if enabled
    )
