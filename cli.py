
"""Command line entry point for Continuum."""

import argparse
import sys

import commands

VERSION = "1_test"


# ---------------------------------------
# Command Configuration
# ---------------------------------------

COMMANDS = [
    {
        "name": "save",
        "help": "Save active terminal programs",
        "handler": commands.save,
    },
    {
        "name": "list",
        "help": "List locally saved sessions",
        "handler": commands.list_sessions,
    },
    {
        "name": "restore",
        "help": "Restore the latest saved session",
        "handler": commands.restore,
    },
    {
        "name": "status",
        "help": "Show current terminal status",
        "handler": commands.status,
    },
    {
        "name": "whitelist",
        "help": "Manage whitelisted programs",
        "handler": commands.whitelist,

        "subcommands": [
            {
                "name": "ls",
                "help": "List whitelisted programs",
                "handler": commands.whitelist_ls,
            },
            {
                "name": "add",
                "help": "Add a program to the whitelist",
                "handler": commands.whitelist_add,
                "arguments": [
                    {
                        "flags": ["program"],
                        "help": "Program to add",
                    }
                ],
            },
            {
                "name": "remove",
                "help": "Remove a program from the whitelist",
                "handler": commands.whitelist_remove,
                "arguments": [
                    {
                        "flags": ["program"],
                        "help": "Program to remove",
                    }
                ],
            },
        ],
    },
    {
        "name":"ssh",
        "help":"Establish or Change ssh connections",
        "handler": commands.show,

        "subcommands": [
            {
                "name":"new",
                "aliases":["add"],
                "help":"Add a SSH connections",
                "handler":commands.new_ssh,

                "arguments":[
                    {
                        "flags":["--name"],
                        "required": True,
                        "help":"set Device Name"
                    },
                    {
                        "flags":["--host"],
                        "required": True,
                        "help":"set Device Host"
                    },
                    {
                        "flags":["--user"],
                        "required": True,
                        "help":"set Device Username (for SSH)"
                    },
                    {
                        "flags":["--port"],
                        "type": int,
                        "default":22,
                        "help":"SSH port setzen"
                    },
                ]
            },
            {
                "name": "remove",
                "aliases": ["rm", "delete"],
                "help": "Remove an SSH device",
                "handler": commands.delete_ssh,
                "arguments": [
                    {
                        "flags": ["name"],
                        "help": "Name of the SSH device or the host"
                    }
                ]
            }
        ]
    },
]


# ---------------------------------------
# Generic Parser Builder
# ---------------------------------------

def register_commands(subparsers, definitions):
    """
    Recursively register commands and subcommands.

    Args:
        subparsers: argparse subparser collection.
        definitions: List of command configurations.
    """

    for definition in definitions:
        parser = subparsers.add_parser(
            definition["name"],
            aliases=definition.get("aliases", []),
            help=definition.get("help", ""),
            description=definition.get("help", "")
        )

        # Register arguments
        for argument in definition.get("arguments", []):
            options = argument.copy()
            flags = options.pop("flags")
            parser.add_argument(*flags, **options)

        # Register handler
        if "handler" in definition:
            parser.set_defaults(
                handler=definition["handler"]
            )

        # Register nested commands
        if "subcommands" in definition:
            nested = parser.add_subparsers(
                dest="action"
            )

            register_commands(
                nested,
                definition["subcommands"]
            )


def create_parser() -> argparse.ArgumentParser:
    """Create the Continuum CLI parser."""

    parser = argparse.ArgumentParser(
        prog="continuum",
        description="Save and restore terminal sessions"
    )

    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"continuum {VERSION}"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    register_commands(subparsers, COMMANDS)

    return parser


# ---------------------------------------
# Entry Point
# ---------------------------------------

def main() -> None:
    """Parse arguments and execute the selected command."""

    parser = create_parser()
    argv = sys.argv[1:]

    # Support: continuum help [COMMAND ...]
    if argv and argv[0] == "help":
        argv = argv[1:] + ["--help"]

    args = parser.parse_args(argv)

    try:
        handler = args.handler

        # Pass only declared command arguments
        kwargs = vars(args).copy()

        kwargs.pop("handler", None)
        kwargs.pop("command", None)
        kwargs.pop("action", None)

        handler(**kwargs)

    except Exception as exc:
        print(f"continuum: {exc}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()

