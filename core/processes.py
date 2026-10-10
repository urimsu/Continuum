"""Funktionen zum Auslesen von Linux-Prozessinformationen über /proc."""

import sys
from pathlib import Path


def get_process_name(pid: int) -> str | None:
    """
    Ermittelt den Namen eines laufenden Linux-Prozesses anhand seiner PID.

    Liest die Datei /proc/<pid>/comm, die den Prozessnamen enthält.

    Args:
        pid (int): Die Prozess-ID des gesuchten Prozesses.

    Returns:
        str | None:
            Den Prozessnamen als String, wenn er gelesen werden konnte.
            None, wenn der Zugriff fehlschlägt oder der Prozess nicht existiert.

    Example:
        >>> get_process_name(1)
        'systemd'
    """
    try:
        path = Path(f"/proc/{pid}/comm")
        return path.read_text().strip()

    except PermissionError:
        print(f"Keine Berechtigung für PID {pid}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Prozess {pid} existiert nicht mehr", file=sys.stderr)

    return None


def get_process_cwd(pid: int) -> str | None:
    """
    Ermittelt das aktuelle Arbeitsverzeichnis eines Linux-Prozesses.

    Liest den symbolischen Link /proc/<pid>/cwd, der auf das
    aktuelle Arbeitsverzeichnis des Prozesses verweist.

    Args:
        pid (int): Die Prozess-ID des gesuchten Prozesses.

    Returns:
        str | None:
            Den absoluten Pfad des Arbeitsverzeichnisses als String.
            None, wenn der Zugriff fehlschlägt oder der Prozess nicht existiert.

    Example:
        >>> get_process_cwd(1234)
        '/home/urim/Continuum'
    """
    try:
        path = Path(f"/proc/{pid}/cwd")
        return str(path.resolve(strict=True))

    except PermissionError:
        print(f"Keine Berechtigung für PID {pid}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Prozess {pid} oder sein Arbeitsverzeichnis existiert nicht mehr", file=sys.stderr)

    return None

def get_parent_pid(pid: int) -> int | None:
    """
    Ermittelt die Elternprozess-ID eines Linux-Prozesses.

    Liest das Feld PPid aus /proc/<pid>/status.

    Args:
        pid: Prozess-ID des untersuchten Prozesses.

    Returns:
        Elternprozess-ID oder None, falls sie nicht gelesen werden kann.
    """
    try:
        path = Path(f"/proc/{pid}/status")

        for line in path.read_text().splitlines():
            if line.startswith("PPid:"):
                return int(line.split()[1])

    except (OSError, ValueError, IndexError):
        return None

    return None

def get_process_cmdline(pid: int) -> list[str] | None:
    """
    Ermittelt die Kommandozeilenargumente eines Linux-Prozesses.

    Liest /proc/<pid>/cmdline. Die Argumente sind durch
    Nullbytes (\0) getrennt.

    Args:
        pid: Prozess-ID des untersuchten Prozesses.

    Returns:
        Liste der Startargumente oder None bei einem Lesefehler.
    """
    try:
        path = Path(f"/proc/{pid}/cmdline")
        content = path.read_bytes()

        if not content:
            return []

        return [
            arg.decode("utf-8", errors="replace")
            for arg in content.rstrip(b"\0").split(b"\0")
        ]

    except (PermissionError, FileNotFoundError) as error:
        print(f"Fehler bei PID {pid}: {error}", file=sys.stderr)
        return None

def get_all_processes() -> list[int]:
    """
      Ermittelt alle aktuell laufenden Prozesse auf einem Linux-System.

      Durchsucht das /proc-Verzeichnis nach Prozess-IDs (PIDs)
      und sammelt Informationen zu den gefundenen Prozessen.

      Returns:
          list[dict]: Eine Liste mit Informationen zu allen
                      erkannten Prozessen.

      Example:
          >>> get_all_processes()
          [
              {"pid": 1, "name": "systemd"},
              {"pid": 1234, "name": "htop"}
          ]
      """
    pids = []

    for entry in Path("/proc").iterdir():
        if entry.name.isdigit():
            pids.append(int(entry.name))

    return sorted(pids)
