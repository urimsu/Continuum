import json
import subprocess
from pathlib import Path
import os
import shutil
import core

import config.whitelist
ALLOWED_PROGRAMS = config.whitelist.get_allowed_programs()

SESSION_FILE = Path.home() / ".local/state/continuum/processes.json"

TERMINAL_PROGRAMS = {
    "nvim", "htop", "btop", "vim", "nano",
    "zsh", "bash", "fish", "sh"
}

TERMINAL_EMULATORS = {
    "kitty", "alacritty", "ghostty", "foot",
    "wezterm", "gnome-terminal", "konsole"
}

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
    Stellt gespeicherte Prozesse wieder her.

    Terminalprozesse werden im bevorzugten
    Terminalemulator des aktuellen Systems gestartet.

    Returns:
        True, wenn alle Prozesse erfolgreich gestartet
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

        if not name or not cmdline:
            continue

        # Prozessnamen aus absoluten Pfaden normalisieren
        name = Path(name).name
        executable = Path(cmdline[0]).name

        if name not in ALLOWED_PROGRAMS:
            continue

        if not cwd or not Path(cwd).is_dir():
            print(f"Ungültiges Arbeitsverzeichnis: {cwd}")
            success = False
            continue

        try:
            if name in TERMINAL_EMULATORS or executable in TERMINAL_EMULATORS:
                terminal = get_default_terminal()

                if terminal is None:
                    print("Kein Terminalemulator gefunden.")
                    success = False
                    continue

                # Gespeicherten Emulator nicht erneut starten
                command = [terminal]

            elif name in TERMINAL_PROGRAMS or executable in TERMINAL_PROGRAMS:
                terminal = get_default_terminal()

                if terminal is None:
                    print("Kein Terminalemulator gefunden.")
                    success = False
                    continue

                # Terminalprogramm im aktuellen Emulator starten
                command = [terminal, "-e", *cmdline]

            else:
                command = cmdline

            subprocess.Popen(
                command,
                cwd=cwd,
                start_new_session=True
            )

            print(f"Gestartet: {name}")

        except OSError as error:
            change_name_or_path()
            print(f"Fehler beim Starten von {name}: {error}")
            print("Try: continuum list --change")

            success = False

    return success


def change_name_or_path():
    try:
        with SESSION_FILE.open("r", encoding="utf-8") as file:
            processes_json = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"Session konnte nicht geladen werden: {error}")
        return False
   
    processes= []

    for index,process in enumerate(processes_json):
        name = process.get("name")
        cwd = process.get("cwd")
        cmdline = process.get("cmdline")
        
        processes.append({"name":name,"cwd":cwd,"cmdline":cmdline})
        print(index, " : ",name, " : ", cwd, " : ", cmdline)

    usr_input=input("There are Processes or Directorys not working. Do you want to change them?[Y|Yes]: ")
    yes=["yes","Yes","y","Y"]

    if(usr_input in yes):
        change_index=input("Press the number and (name || cwd) and the change. e.g. \"1 name firefox\": ")
        
        change_index=change_index.split()
        
        process_number=int(change_index[0])
        process_operation = change_index[1]
        process_change=change_index[2]

        processes[process_number][process_operation]=process_change
    else:
        print("nicht aendern")


    with SESSION_FILE.open("w", encoding="utf-8") as f:
        json.dump(processes, f, indent=4)
