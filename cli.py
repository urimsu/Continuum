
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

    whitelist = sub.add_parser("whitelist", help="Manage Whitelists")
    # Whitelist-Unterbefehle
    whitelist_sub = whitelist.add_subparsers(dest="action", required=False)

    whitelist_sub.add_parser("ls", help="List whitelisted programs")

    add = whitelist_sub.add_parser("add", help="Add program to whitelist")
    add.add_argument("program", help="Program to add")

    remove = whitelist_sub.add_parser("remove", help="Remove program from whitelist")
    remove.add_argument("program", help="Program to remove")

    return result


def main() -> None:
    cli = parser()
    argv = sys.argv[1:]
    # Clap provides `continuum help [COMMAND]`; keep that built-in interface.
    if argv == ["help"]:
        cli.print_help()
        return
    if len(argv) == 2 and argv[0] == "help" and argv[1] in {"save", "list", "restore", "status","whitelist"}:
        parser_for_command = argparse.ArgumentParser(prog=f"continuum {argv[1]}")
        descriptions = {
            "save": "Detect terminal windows and save their active foreground programs",
            "list": "List locally saved sessions",
            "restore": "Preview and interactively restore the latest saved session",
            "status": "Show detected terminal windows and the latest saved session",
            "whitelist": "Show all currently whitelisted programs",
            "whitelist ls": "List running programs available to add to the whitelist",
            "whitelist add": "Add a program to the whitelist",
            "whitelist remove": "Remove a program from the whitelist",
        }

        if argv == ["help"]:
            cli.print_help()
            return

        if argv and argv[0] == "help":
            command = " ".join(argv[1:])

        if command in descriptions:
            parser_for_command = argparse.ArgumentParser(
                prog=f"continuum {command}",
                description=descriptions[command]
            )

        if command in {"whitelist add", "whitelist remove"}:
            parser_for_command.add_argument(
                "program",
                help="Name of the program"
            )

        parser_for_command.print_help()
        return
    args = cli.parse_args(argv)
    try:
        if args.command == "list":
            commands.list_sessions()
        else:
            {
                "save": lambda: commands.save(),
                "restore": lambda: commands.restore(),
                "status": lambda: commands.status(),
                "whitelist": lambda: {
                    None:lambda: commands.whitelist(),
                    "ls": lambda: commands.whitelist_ls(),
                    "add": lambda: commands.whitelist_add(args.program),
                    "remove": lambda: commands.whitelist_remove(args.program)
                }[args.action]()
            }[args.command]() 
    except Exception as exc:
        print(f"continuum: {exc}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
