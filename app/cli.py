"""Command-line interface for secure password generation."""

from __future__ import annotations

import argparse

from app.generator import generate_password
from app.validators import is_password_valid


def _prompt_mode() -> str:
    """Prompt the user to choose manual or automatic mode."""
    while True:
        choice = input(
            "Choose mode: [1] automatic generation or [2] manual password: "
        ).strip()

        if choice == "1":
            return "automatic"
        if choice == "2":
            return "manual"

        print("Invalid option. Enter 1 for automatic or 2 for manual.")


def _resolve_character_options(args: argparse.Namespace) -> dict[str, bool]:
    """Resolve CLI flags into generator options.

    If no character type is explicitly selected, all types are enabled.
    """
    selected_any = any(
        [args.uppercase, args.lowercase, args.numbers, args.symbols]
    )

    if not selected_any:
        return {
            "uppercase": True,
            "lowercase": True,
            "numbers": True,
            "symbols": True,
        }

    return {
        "uppercase": args.uppercase,
        "lowercase": args.lowercase,
        "numbers": args.numbers,
        "symbols": args.symbols,
    }


def _resolve_mode(args: argparse.Namespace) -> str:
    """Resolve the CLI mode from args or interactive prompt."""
    if args.password is not None:
        return "manual"

    if args.mode is not None:
        return args.mode

    return _prompt_mode()


def _resolve_password(
    args: argparse.Namespace,
    character_options: dict[str, bool],
    mode: str,
) -> str:
    """Return a manual password or generate one automatically."""
    if mode == "manual":
        if args.password is not None:
            return args.password

        return input("Enter your password: ").strip()

    if args.password is not None:
        return args.password

    return generate_password(
        length=args.length,
        uppercase=character_options["uppercase"],
        lowercase=character_options["lowercase"],
        numbers=character_options["numbers"],
        symbols=character_options["symbols"],
    )


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate cryptographically secure passwords."
    )
    parser.add_argument(
        "--mode",
        choices=["automatic", "manual"],
        help="Choose the execution mode.",
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Use a manually provided password instead of generating one.",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=16,
        help="Password length. Default: 16.",
    )
    parser.add_argument(
        "--uppercase",
        action="store_true",
        help="Include uppercase letters.",
    )
    parser.add_argument(
        "--lowercase",
        action="store_true",
        help="Include lowercase letters.",
    )
    parser.add_argument(
        "--numbers",
        action="store_true",
        help="Include numbers.",
    )
    parser.add_argument(
        "--symbols",
        action="store_true",
        help="Include symbols.",
    )
    return parser


def main() -> None:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args()
    character_options = _resolve_character_options(args)
    mode = _resolve_mode(args)
    password = _resolve_password(args, character_options, mode)
    is_valid = is_password_valid(
        password=password,
        uppercase=character_options["uppercase"],
        lowercase=character_options["lowercase"],
        numbers=character_options["numbers"],
        symbols=character_options["symbols"],
    )

    print(f"Password: {password}")
    print(f"Mode: {mode}")
    print(f"Validation: {'valid' if is_valid else 'invalid'}")


if __name__ == "__main__":
    main()
