import json
import subprocess
from pathlib import Path
import os
import shutil

import config.whitelist
ALLOWED_PROGRAMS = config.whitelist.get_allowed_programs()

SESSION_FILE = Path.home() / ".local/state/continuum/processes.json"

TERMINAL_PROGRAMS = {"nvim", "htop", "btop", "vim", "nano"}

def get_default_terminal() -> str | None:
    """
    Ermittelt einen verfügbaren Terminalemulator.

    Returns:
        Name oder Pfad des Terminalemulators.
        None, wenn keiner gefunden wurde.
    """

    terminal = os.environ.get("TERMINAL")

    if terminal and shutil.which(terminal):
        return terminal

    terminals = [
        "ghostty",
        "kitty",
        "alacritty",
        "foot",
        "wezterm",
        "gnome-terminal",
        "konsole"
    ]

    for name in terminals:
        if shutil.which(name):
            return name

    return None
def launch_processes() -> bool:
    """
    Liest gespeicherte Prozesse aus der JSON-Datei
    und startet erlaubte Programme erneut.

    Terminalprogramme werden in Kitty geöffnet.
    Das ursprüngliche Arbeitsverzeichnis wird übernommen.

    Returns:
        True, wenn alle ausgewählten Prozesse gestartet
        werden konnten, andernfalls False.
    """

    try:
        with SESSION_FILE.open("r", encoding="utf-8") as file:
            processes = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"Session konnte nicht geladen werden: {error}")
        return False

    success = True

    for process in processes:
        name = process.get("name")
        cwd = process.get("cwd")
        cmdline = process.get("cmdline")

        if name not in ALLOWED_PROGRAMS:
            continue

        if not cmdline:
            continue

        if not cwd or not Path(cwd).is_dir():
            print(f"Ungültiges Arbeitsverzeichnis: {cwd}")
            success = False
            continue

        try:
            if name in TERMINAL_PROGRAMS:
                terminal = get_default_terminal()

                if terminal is None:
                    print("Kein Terminalemulator gefunden.")
                    success = False
                    continue

                subprocess.Popen(
                    [terminal, *cmdline],
                    cwd=cwd,
                    start_new_session=True
                )
            else:
                subprocess.Popen(
                    cmdline,
                    cwd=cwd
                )

            print(f"Gestartet: {name}")

        except OSError as error:
            print(f"Fehler beim Starten von {name}: {error}")
            success = False

    return success
