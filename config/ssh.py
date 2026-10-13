import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".config/continuum/devices.json"

CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

def show_ssh_list() -> list[dict]:
    """
    Return all configured SSH devices.

    Returns:
        List of SSH device dictionaries.
        Empty list if no configuration exists.
    """
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        devices = data.get("devices", [])

        # Compatibility with old configuration
        if isinstance(devices, dict):
            return [devices]

        return devices

    except (FileNotFoundError, json.JSONDecodeError):
        return []

def add_ssh_device(
    name: str,
    host: str,
    user: str,
    port: int = 22
) -> bool:
    """
    Add a new SSH device to the configuration.

    Args:
        name: Unique device name.
        host: IP address or hostname.
        user: SSH username.
        port: SSH port (default: 22).

    Returns:
        True if device was saved successfully.

    Raises:
        ValueError: If a device with the same name exists.
    """

    devices = show_ssh_list()

    # Prevent duplicate device names
    if any(device["name"] == name for device in devices):
        raise ValueError(f"SSH device '{name}' already exists")

    device = {
        "name": name,
        "host": host,
        "user": user,
        "port": port
    }

    devices.append(device)

    CONFIG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"devices": devices},
            file,
            indent=4
        )

    return True

def remove_ssh_device(name: str) -> bool:
    """
    Remove an SSH device by name or host.

    Args:
        name: Device name or host/IP address.

    Returns:
        True if the device was removed successfully.

    Raises:
        ValueError: If no matching device exists.
    """

    devices = show_ssh_list()

    # Find devices matching name or host
    matches = [
        device for device in devices
        if device["name"] == name or device["host"] == name
    ]

    if not matches:
        raise ValueError(f"SSH device '{name}' does not exist")

    # Prevent accidentally removing multiple devices
    if len(matches) > 1:
        raise ValueError(
            f"Multiple SSH devices match '{name}'. "
            "Please use a unique device name or host."
        )

    devices.remove(matches[0])

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"devices": devices},
            file,
            indent=4
        )

    return True
