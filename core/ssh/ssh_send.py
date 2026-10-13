import subprocess
from pathlib import Path

from config import ssh as ssh_config

SESSION_FILE = Path.home() / ".local/state/continuum/processes.json"


def send_session(
    remote_user: str,
    remote_host: str,
    remote_path: str,
    local_path: str = SESSION_FILE
) -> None:
    """
    Transfers a locally saved Continuum session to a remote device via SCP (SSH).

    The function executes the system's SCP command using subprocess.
    The remote device must be reachable via SSH and the destination
    directory must already exist.

    Args:
        remote_user (str):
            Required. SSH username on the remote device.

        remote_host (str):
            Required. IP address or hostname of the remote device.

        remote_path (str):
            Required. Destination path on the remote device.

        local_path (str):
            Optional. Path to the local session file.
            Defaults to SESSION_FILE.

    Returns:
        None:
            Does not return a value.

    Raises:
        subprocess.CalledProcessError:
            If the SCP transfer fails.

        FileNotFoundError:
            If the SCP executable cannot be found.
    """

    _ = subprocess.run(
        [
            "scp",
            local_path,
            f"{remote_user}@{remote_host}:{remote_path}"
        ],
        check=True
    )

def send_all_sessions(
    remote_path: str = "~/.local/state/continuum/processes.json"
) -> dict[str, bool]:
    """
    Send the current session to all configured SSH devices.

    Args:
        remote_path: Destination path on remote devices.

    Returns:
        Dictionary mapping device names to transfer success.
    """

    devices = ssh_config.show_ssh_list()
    results = {}

    for device in devices:
        name = device["name"]

        try:
            send_session(
                remote_user=device["user"],
                remote_host=device["host"],
                remote_path=remote_path
            )

            results[name] = True

        except (subprocess.CalledProcessError, OSError):
            results[name] = False

    return results
