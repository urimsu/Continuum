import subprocess

from config.whitelist import ALLOWED_PROGRAMS, BLACKLISTED_PROGRAMS


def launch_process(name: str, cwd: str) -> bool:
    """
    Startet ein erlaubtes Terminalprogramm in einem neuen Alacritty-Fenster.

    Args:
        name: Name des Programms, z. B. 'btop'.
        cwd: Arbeitsverzeichnis des Programms.

    Returns:
        True, wenn der Start des Terminalprozesses erfolgreich
        angestoßen wurde, andernfalls False.
    """
    if name not in ALLOWED_PROGRAMS or name in BLACKLISTED_PROGRAMS:
        print(f"Programm '{name}' ist nicht erlaubt.")
        return False

    try:
        subprocess.Popen(
            ["alacritty", "--working-directory", cwd, "-e", name]
        )
        return True

    except OSError as error:
        print(f"Programm konnte nicht gestartet werden: {error}")
        return False
