import os
import json
from pathlib import Path
from datetime import datetime

STATE_DIR = (
    Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
    / "continuum"
)

STATE_DIR.mkdir(parents=True, exist_ok=True)

PROCESSES_FILE = STATE_DIR / "processes.json"

def save_processes(processes: list):
    with PROCESSES_FILE.open("w", encoding="utf-8") as f:
        json.dump(processes, f, indent=4)

def read_stored_processes() -> list[dict]:
    """
    Liest die gespeicherten Prozesse aus der Session-JSON-Datei.

    Returns:
        list[dict]: Liste der gespeicherten Prozesse.
                    Leere Liste, falls keine Session vorhanden ist.
    """
    try:
        with PROCESSES_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def read_session_date() -> str | None:
    """
    Liest Datum und Uhrzeit der letzten Änderung der Session-Datei.

    Returns:
        str | None: Datum und Uhrzeit der letzten Änderung.
                    None, falls die Datei nicht existiert.
    """
    try:
        timestamp = PROCESSES_FILE.stat().st_mtime
        return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M:%S")

    except FileNotFoundError:
        return None
