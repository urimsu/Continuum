import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".config/continuum/whitelist.json"

CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

def get_allowed_programs() -> set[str]:
    """
    Liest die erlaubten Programme aus der Whitelist-JSON.

    Returns:
        set[str]: Menge aller erlaubten Programme.
                  Leere Menge, wenn die Datei nicht existiert.
    """
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return set(data.get("allowed_programs", []))

    except (FileNotFoundError, json.JSONDecodeError):
        return set()



def add_allowed_program(program: str) -> bool:
    """
    Fügt ein Programm zur Whitelist hinzu.

    Args:
        program: Name des Programms.

    Returns:
        True, wenn das Programm hinzugefügt wurde.
        False, wenn es bereits existiert.
    """
    programs = get_allowed_programs()

    if program in programs:
        return False

    programs.add(program)

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"allowed_programs": sorted(programs)},
            file,
            indent=4
        )

    return True


def remove_allowed_program(program: str) -> bool:
    """
    Entfernt ein Programm aus der Whitelist.

    Args:
        program: Name des Programms.

    Returns:
        True, wenn das Programm entfernt wurde.
        False, wenn es nicht in der Whitelist existiert.
    """
    programs = get_allowed_programs()

    if program not in programs:
        return False

    programs.remove(program)

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"allowed_programs": sorted(programs)},
            file,
            indent=4
        )

    return True
