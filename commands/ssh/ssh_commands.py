import config.ssh as ssh_config

# Global Colors
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
GRAY = "\033[90m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"
BLUE = "\033[36m"
LIGHT_RED = "\033[31m"


def show() -> None:
    """Display all configured SSH devices in a formatted list."""

    devices = ssh_config.show_ssh_list()

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"  {CYAN}Continuum{RESET}  /  SSH Devices")
    print(f"{CYAN}{'─' * 55}{RESET}\n")

    if not devices:
        print(f"  {YELLOW}●{RESET}  No SSH devices configured.\n")
        return

    for index, device in enumerate(devices, start=1):
        name = device.get("name", "Unknown")
        host = device.get("host", "N/A")
        user = device.get("user", "N/A")
        port = device.get("port", 22)

        print(f"  {GREEN}●{RESET}  {index}. {name}")
        print(f"     {GRAY}Host     {RESET}{host}")
        print(f"     {GRAY}User     {RESET}{user}")
        print(f"     {GRAY}Port     {RESET}{port}")
        print()

    print(f"{CYAN}{'─' * 55}{RESET}")
    print(f"  {GRAY}Total devices: {len(devices)}{RESET}")
    print(f"{CYAN}{'─' * 55}{RESET}\n")


def new_ssh(
    name: str,
    host: str,
    user: str,
    port: int = 22
) -> None:
    """Add a new SSH device and display a confirmation."""

    ssh_config.add_ssh_device(name, host, user, port)

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"  {CYAN}Continuum{RESET}  /  SSH Devices")
    print(f"{CYAN}{'─' * 55}{RESET}\n")

    print(f"  {GREEN}✓  SSH device added successfully!{RESET}\n")

    print(f"  {GREEN}●{RESET}  {name}")
    print(f"     {GRAY}Host     {RESET}{host}")
    print(f"     {GRAY}User     {RESET}{user}")
    print(f"     {GRAY}Port     {RESET}{port}")

    print(f"\n{CYAN}{'─' * 55}{RESET}\n")


def change_ssh_name():
    return

def change_ssh_host():
    return

def change_ssh_user():
    return

def change_ssh_port():
    return


def delete_ssh(name: str) -> None:
    """Remove an SSH device and display a confirmation."""

    ssh_config.remove_ssh_device(name)

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"  {CYAN}Continuum{RESET}  /  SSH Devices")
    print(f"{CYAN}{'─' * 55}{RESET}\n")

    print(f"  {GREEN}✓  SSH device removed successfully!{RESET}\n")

    print(f"  {RED}●{RESET}  {name}")
    print(f"     {GRAY}Status   {RESET}{LIGHT_RED}Removed{RESET}")

    print(f"\n{CYAN}{'─' * 55}{RESET}\n")

