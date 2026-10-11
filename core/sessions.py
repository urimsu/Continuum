import os
import json
from pathlib import Path

STATE_DIR = (
    Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
    / "continuum"
)

STATE_DIR.mkdir(parents=True, exist_ok=True)

PROCESSES_FILE = STATE_DIR / "processes.json"

def save_processes(processes: list):
    with PROCESSES_FILE.open("w", encoding="utf-8") as f:
        json.dump(processes, f, indent=4)
