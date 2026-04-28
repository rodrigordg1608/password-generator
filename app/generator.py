"""Password generation helpers."""

from __future__ import annotations

import secrets
import string

from app.validators import validate_password_options


def _build_character_groups(
    uppercase: bool,
    lowercase: bool,
    numbers: bool,
    symbols: bool,
) -> list[str]:
    """Return the selected character groups."""
    groups: list[str] = []

    if uppercase:
        groups.append(string.ascii_uppercase)
    if lowercase:
        groups.append(string.ascii_lowercase)
    if numbers:
        groups.append(string.digits)
    if symbols:
        groups.append(string.punctuation)

    return groups


def _choose_one_from_each_group(groups: list[str]) -> list[str]:
    """Return one secure random character for each selected group."""
    return [secrets.choice(group) for group in groups]


def _shuffle_characters(characters: list[str]) -> str:
    """Securely shuffle characters and return the final password."""
    shuffled = characters[:]
    secrets.SystemRandom().shuffle(shuffled)
    return "".join(shuffled)


def generate_password(
    length: int,
    uppercase: bool = True,
    lowercase: bool = True,
    numbers: bool = True,
    symbols: bool = True,
) -> str:
    """Generate a cryptographically secure password.

    The generated password always includes at least one character from each
    selected group.
    """
    groups = _build_character_groups(
        uppercase=uppercase,
        lowercase=lowercase,
        numbers=numbers,
        symbols=symbols,
    )
    validate_password_options(length=length, groups=groups)

    password_characters = _choose_one_from_each_group(groups)
    all_characters = "".join(groups)

    while len(password_characters) < length:
        password_characters.append(secrets.choice(all_characters))

    return _shuffle_characters(password_characters)
