"""Funktionen zum Auslesen von Linux-Prozessinformationen über /proc."""

import sys
import os
from pathlib import Path

SYSTEM_PROCESSES = {
    # Systemdienste
    "systemd",
    "systemctl",
    "(sd-pam)",
    "cupsd",
    "dconf-service",
    "fcitx5",
    "bt-agent",
    "power-profiles-",
    "udiskie",
    "uwsm",
    "start-hyprland",

    # Desktop-Dienste
    "at-spi-bus-laun",
    "at-spi2-registr",
    "gnome-keyring-d",
    "quickshell",
    "wl-paste",
    "inotifywait",
    "socat",
    "waitpid",
    "fusermount3",

    # Browser-Hilfsprozesse
    "Isolated Servic",
    "Isolated Web Co",
    "Privileged Cont",
    "RDD Process",
    "Socket Process",
    "Utility Process",
    "Web Content",
    "WebExtensions",
    "chrome_crashpad",
    "forkserver",

    # Sonstige
    "localsearch-3",
    "localsearch-ext",
    "codex-code-mode",

    # Displayserver / Window Manager
    "Hyprland",
    "Xwayland",
    "sway",
    "waybar",
    "quickshell",

    # Audio
    "pipewire",
    "pipewire-pulse",
    "wireplumber",

    # Systemtools
    "journalctl",
    "systemctl",
    "wl-copy",
    "wl-paste",
    "sh",
    "bash",
    "zsh",

    # Weitere Hintergrundprozesse
    "dbus-broker",
    "NetworkManager",
    "systemd",
    "polkitd",
    "udisksd",
    "upowerd",
}

SYSTEM_PREFIXES = (
    "systemd",
    "kworker",
    "ksoftirqd",
    "migration/",
    "cpuhp/",
    "irq/",
    "rcu",
    "nvidia",
    "nv_",
    "watchdog",
    "idle_inject",
    "dbus-",
    "xdg-",
    "gvfs",
    "omarchy-",
    "at-spi",
)

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

def get_all_processes_names() -> list[str]:
    """
    Ermittelt laufende Benutzerprogramme unter Linux.

    Filtert:
    - Kernel-Threads
    - Prozesse anderer Benutzer
    - Bekannte Systemprozesse
    - Hintergrund- und Hilfsprozesse
    - Doppelte Prozessnamen

    Returns:
        list[str]: Alphabetisch sortierte Prozessnamen.
    """
    process_names = set()
    current_uid = os.getuid()

    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue

        try:
            # Nur Prozesse des aktuellen Benutzers
            if entry.stat().st_uid != current_uid:
                continue

            # Kernel-Threads ausschließen
            cmdline = (entry / "cmdline").read_bytes()

            if not cmdline:
                continue

            name = (entry / "comm").read_text().strip()

            # Systemprozesse ausschließen
            if name in SYSTEM_PROCESSES:
                continue

            # Systemprozess-Präfixe ausschließen
            if name.startswith(SYSTEM_PREFIXES):
                continue

            process_names.add(name)

        except (OSError, ProcessLookupError):
            continue

    return sorted(process_names)
