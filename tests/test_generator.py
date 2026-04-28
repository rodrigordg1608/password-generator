"""Tests for secure password generation."""

from argparse import Namespace
import string

import pytest

from app.cli import _resolve_mode, _resolve_password
from app.generator import generate_password
from app.validators import is_password_valid


def test_generate_password_returns_requested_length() -> None:
    """Password should have the requested length."""
    password = generate_password(length=20)

    assert len(password) == 20


def test_generate_password_includes_required_character_types() -> None:
    """Password should include at least one character from each type."""
    password = generate_password(
        length=12,
        uppercase=True,
        lowercase=True,
        numbers=True,
        symbols=True,
    )

    assert any(char in string.ascii_uppercase for char in password)
    assert any(char in string.ascii_lowercase for char in password)
    assert any(char in string.digits for char in password)
    assert any(char in string.punctuation for char in password)


def test_generate_password_returns_different_values_across_runs() -> None:
    """Password generation should produce different values in distinct runs."""
    first_password = generate_password(length=16)
    second_password = generate_password(length=16)

    assert first_password != second_password


def test_generate_password_raises_for_invalid_minimum_length() -> None:
    """Password generation should reject lengths smaller than four."""
    with pytest.raises(ValueError, match="at least 4 characters"):
        generate_password(length=3)


def test_generate_password_raises_without_selected_character_types() -> None:
    """Password generation should reject requests without character types."""
    with pytest.raises(ValueError, match="at least one character type"):
        generate_password(
            length=8,
            uppercase=False,
            lowercase=False,
            numbers=False,
            symbols=False,
        )


def test_is_password_valid_returns_true_for_generated_password() -> None:
    """Generated password should pass validation for the selected rules."""
    password = generate_password(
        length=12,
        uppercase=True,
        lowercase=True,
        numbers=True,
        symbols=False,
    )

    assert is_password_valid(
        password=password,
        uppercase=True,
        lowercase=True,
        numbers=True,
        symbols=False,
    )


def test_is_password_valid_returns_false_when_required_type_is_missing() -> None:
    """Validation should fail when a required character type is missing."""
    assert not is_password_valid(
        password="abc123def456",
        uppercase=True,
        lowercase=True,
        numbers=True,
        symbols=False,
    )


def test_resolve_password_returns_manual_password_when_provided() -> None:
    """CLI should use the manually provided password when available."""
    args = Namespace(password="MinhaSenha123!", length=16, mode=None)

    password = _resolve_password(
        args=args,
        character_options={
            "uppercase": True,
            "lowercase": True,
            "numbers": True,
            "symbols": True,
        },
        mode="manual",
    )

    assert password == "MinhaSenha123!"


def test_resolve_password_generates_password_when_not_provided() -> None:
    """CLI should generate a password when no manual value is provided."""
    args = Namespace(password=None, length=10, mode=None)

    password = _resolve_password(
        args=args,
        character_options={
            "uppercase": True,
            "lowercase": False,
            "numbers": True,
            "symbols": False,
        },
        mode="automatic",
    )

    assert len(password) == 10
    assert any(char in string.ascii_uppercase for char in password)
    assert any(char in string.digits for char in password)


def test_resolve_mode_returns_manual_when_password_is_provided() -> None:
    """CLI should use manual mode when a password argument is provided."""
    args = Namespace(password="MinhaSenha123!", mode=None)

    assert _resolve_mode(args) == "manual"


def test_resolve_mode_returns_explicit_mode() -> None:
    """CLI should respect the mode provided by CLI arguments."""
    args = Namespace(password=None, mode="automatic")

    assert _resolve_mode(args) == "automatic"


def test_resolve_password_prompts_for_manual_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """CLI should prompt for a password in manual mode."""
    args = Namespace(password=None, length=10, mode="manual")
    monkeypatch.setattr("builtins.input", lambda _: "SenhaManual123!")

    password = _resolve_password(
        args=args,
        character_options={
            "uppercase": True,
            "lowercase": True,
            "numbers": True,
            "symbols": True,
        },
        mode="manual",
    )

    assert password == "SenhaManual123!"
