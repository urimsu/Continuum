
import config.whitelist
import core.processes
import core.launcher
import core.sessions
import core.ssh.ssh_send

# Global Colors
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
GRAY = "\033[90m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"
BLUE = "\033[36m"
LIGHT_RED = "\033[31m"

# Global Whitelist
ALLOWED_PROGRAMS = config.whitelist.get_allowed_programs()


def list_sessions():
    processes = core.sessions.read_stored_processes()
    session_date = core.sessions.read_session_date()

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"  {CYAN}Continuum{RESET}  /  Saved Processes  /  {RED}{session_date or 'Unknown'}{RESET}")
    print(f"{CYAN}{'─' * 55}{RESET}\n")

    if not processes:
        print(f"  {GRAY}No saved processes found.{RESET}\n")
        return

    for index, process in enumerate(processes, start=1):
        name = process.get("name", "Unknown")
        pid = process.get("pid", "N/A")
        cwd = process.get("cwd") or "N/A"
        cmdline = process.get("cmdline") or []

        print(f"  {GREEN}●{RESET}  {index}. {name}")
        print(f"     {GRAY}PID      {pid}{RESET}")
        print(f"     {GRAY}CWD      {cwd}{RESET}")
        print(f"     {GRAY}Command  {' '.join(cmdline)}{RESET}")
        print()

    print(f"{CYAN}{'─' * 55}{RESET}")
    print(f"  {GREEN}✓{RESET} {len(processes)} saved process(es)")
    print(f"{CYAN}{'─' * 55}{RESET}\n")


def status():
    for pid in core.processes.get_all_processes():
        try:
            name = core.processes.get_process_name(pid)

            if name not in ALLOWED_PROGRAMS:
                continue

            cwd = core.processes.get_process_cwd(pid)
            ppid = core.processes.get_parent_pid(pid)
            cmdline = core.processes.get_process_cmdline(pid)

            print(f"\n{CYAN}{'─' * 55}{RESET}")
            print(f"  {GREEN}● {name}{RESET}  {GRAY}(PID: {pid}){RESET}")
            print(f"{CYAN}{'─' * 55}{RESET}")
            print(f"  {GRAY}Working Dir:{RESET}  {cwd}")
            print(f"  {GRAY}Parent PID: {RESET}  {ppid}")
            print(f"  {GRAY}Command:    {RESET}  {cmdline}")

        except (OSError, ProcessLookupError):
            continue


def save():
    processes = []
    tmp_int_negative = 0
    tmp_int_positive = 0

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"{CYAN}  CONTINUUM  |  Save Session{RESET}")
    print(f"{CYAN}{'─' * 55}{RESET}")

    for pid in core.processes.get_all_processes():
        name = core.processes.get_process_name(pid)

        if name in ALLOWED_PROGRAMS:
            cwd = core.processes.get_process_cwd(pid)
            cmdline = core.processes.get_process_cmdline(pid)
            ppid = core.processes.get_parent_pid(pid)

            processes.append({
                "pid": pid,
                "name": name,
                "PPid": ppid,
                "cwd": cwd,
                "cmdline": cmdline
            })

            tmp_int_positive += 1
        else:
            tmp_int_negative += 1

    for i in processes:
        print(f"\n  {GREEN}● {i['name']}{RESET}  {GRAY}(PID: {i['pid']}){RESET}")
        print(f"    {GRAY}Working Dir:{RESET}  {i['cwd']}")
        print(f"    {GRAY}Parent PID: {RESET}  {i['PPid']}")
        print(f"    {GRAY}Command:    {RESET}  {i['cmdline']}")

    core.sessions.save_processes(processes)

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"  {GREEN}✓ Session saved successfully{RESET}")
    print(f"  {GRAY}Saved:    {RESET} {GREEN}{tmp_int_positive}{RESET} processes")
    print(f"  {GRAY}Discarded:{RESET} {YELLOW}{tmp_int_negative}{RESET} processes")
    print(f"{CYAN}{'─' * 55}{RESET}\n")

    results = core.ssh.ssh_send.send_all_sessions()

    for name, success in results.items():
        if success:
            print(f"{GREEN}✓{RESET} Session sent to {name}")
        else:
            print(f"{RED}✗{RESET} Failed to send session to {name}")

    #core.ssh.ssh_send.send_session()

def restore():
    processes = core.sessions.read_stored_processes()

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"{CYAN}  CONTINUUM  |  Restore Session{RESET}")
    print(f"{CYAN}{'─' * 55}{RESET}")

    if not processes:
        print(f"\n  {YELLOW}! No saved processes found.{RESET}")
    else:
        print(f"\n  {GRAY}Found {len(processes)} saved processes:{RESET}")

        for process in processes:
            print(f"\n  {GREEN}● {process['name']}{RESET}")
            print(f"    {GRAY}Working Dir:{RESET}  {process['cwd']}")
            print(f"    {GRAY}Command:    {RESET}  {process['cmdline']}")

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"  {GRAY}Total processes:{RESET} {CYAN}{len(processes)}{RESET}")
    print(f"{CYAN}{'─' * 55}{RESET}\n")
    #core.launcher.change_name_or_path()
    core.launcher.launch_processes()

def update_session() -> None:
    """
    Aktualisiert die Attribute einer gespeicherten Session.

    Ermöglicht das Ändern des Namens oder Pfads einer Session.
    Zeigt den Fortschritt und eine Erfolgsmeldung an.

    Returns:
        None
    """
    print(f"\n{CYAN}◆ Change Session Attributes{RESET}")
    print(f"{GRAY}  Modify session name or path...{RESET}\n")

    core.launcher.change_name_or_path()

    print(f"\n{GREEN}✔ Done!{RESET}")
    print(f"{GRAY}  Session attributes updated successfully.{RESET}\n")

