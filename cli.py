
"""Command line entry point."""
import argparse
import sys

import commands

def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="continuum", description="Save and restore terminal sessions")
    result.add_argument("-V", "--version", action="version", version="continuum Version 1_test") # {__version__}")
    sub = result.add_subparsers(dest="command", required=True)
    sub.add_parser("save", help="Detect terminal windows and save their active foreground programs")
    sub.add_parser("list", help="List locally saved sessions")
    sub.add_parser("restore", help="Preview and interactively restore the latest saved session")
    sub.add_parser("status", help="Show detected terminal windows and the latest saved session")
    return result


def main() -> None:
    cli = parser()
    argv = sys.argv[1:]
    # Clap provides `continuum help [COMMAND]`; keep that built-in interface.
    if argv == ["help"]:
        cli.print_help()
        return
    if len(argv) == 2 and argv[0] == "help" and argv[1] in {"save", "list", "restore", "status"}:
        parser_for_command = argparse.ArgumentParser(prog=f"continuum {argv[1]}")
        descriptions = {
            "save": "Detect terminal windows and save their active foreground programs",
            "list": "List locally saved sessions",
            "restore": "Preview and interactively restore the latest saved session",
            "status": "Show detected terminal windows and the latest saved session",
        }
        parser_for_command.description = descriptions[argv[1]]
        parser_for_command.print_help()
        return
    args = cli.parse_args(argv)
    try:
        if args.command == "list":
            commands.list_sessions()
        else:
            {"save": lambda: commands.save(),
                "restore": lambda: commands.restore(),
                "status": lambda: commands.status()}[args.command]()
    except Exception as exc:
        print(f"continuum: {exc}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
