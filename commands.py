import config.whitelist
import core.processes
import core.launcher
import core.sessions
import shutil

def list_sessions():
    processes = core.sessions.read_stored_processes()
    session_date = core.sessions.read_session_date()

    CYAN = "\033[1;36m"
    GREEN = "\033[1;32m"
    RED = "\033[1;31m"
    GRAY = "\033[90m"
    RESET = "\033[0m"

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
    allowed_programs = config.whitelist.get_allowed_programs()
    for pid in core.processes.get_all_processes():
        try:
            name = core.processes.get_process_name(pid)

            if name not in allowed_programs:
                continue

            cwd = core.processes.get_process_cwd(pid)
            ppid = core.processes.get_parent_pid(pid)
            cmdline = core.processes.get_process_cmdline(pid)

            print(f"\n\033[1;36m{'─' * 55}\033[0m")
            print(f"  \033[1;32m● {name}\033[0m  \033[90m(PID: {pid})\033[0m")
            print(f"\033[1;36m{'─' * 55}\033[0m")
            print(f"  \033[90mWorking Dir:\033[0m  {cwd}")
            print(f"  \033[90mParent PID: \033[0m  {ppid}")
            print(f"  \033[90mCommand:    \033[0m  {cmdline}")

        except (OSError, ProcessLookupError):
            continue

def save():
    processes = []
    tmp_int_negative = 0
    tmp_int_positive = 0

    allowed_programs = get_allowed_programs()

    print(f"\n\033[1;36m{'─' * 55}\033[0m")
    print("\033[1;36m  CONTINUUM  |  Save Session\033[0m")
    print(f"\033[1;36m{'─' * 55}\033[0m")

    for pid in core.processes.get_all_processes():
        name = core.processes.get_process_name(pid)

        if name in allowed_programs:
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
        print(f"\n  \033[1;32m● {i['name']}\033[0m  \033[90m(PID: {i['pid']})\033[0m")
        print(f"    \033[90mWorking Dir:\033[0m  {i['cwd']}")
        print(f"    \033[90mParent PID: \033[0m  {i['PPid']}")
        print(f"    \033[90mCommand:    \033[0m  {i['cmdline']}")

    core.sessions.save_processes(processes)

    print(f"\n\033[1;36m{'─' * 55}\033[0m")
    print("  \033[1;32m✓ Session saved successfully\033[0m")
    print(f"  \033[90mSaved:    \033[0m \033[1;32m{tmp_int_positive}\033[0m processes")
    print(f"  \033[90mDiscarded:\033[0m \033[1;33m{tmp_int_negative}\033[0m processes")
    print(f"\033[1;36m{'─' * 55}\033[0m\n")


def restore():
    processes = core.sessions.read_stored_processes()

    print(f"\n\033[1;36m{'─' * 55}\033[0m")
    print("\033[1;36m  CONTINUUM  |  Restore Session\033[0m")
    print(f"\033[1;36m{'─' * 55}\033[0m")

    if not processes:
        print("\n  \033[1;33m! No saved processes found.\033[0m")
    else:
        print(f"\n  \033[90mFound {len(processes)} saved processes:\033[0m")

        for process in processes:
            print(f"\n  \033[1;32m● {process['name']}\033[0m")
            print(f"    \033[90mWorking Dir:\033[0m  {process['cwd']}")
            print(f"    \033[90mCommand:    \033[0m  {process['cmdline']}")

    print(f"\n\033[1;36m{'─' * 55}\033[0m")
    print(f"  \033[90mTotal processes:\033[0m \033[1;36m{len(processes)}\033[0m")
    print(f"\033[1;36m{'─' * 55}\033[0m\n")

    core.launcher.launch_processes()


def whitelist():
    programs = sorted(config.whitelist.get_allowed_programs())

    print(f"\n\033[1;36m{'─' * 55}\033[0m")
    print("\033[1;36m  CONTINUUM  |  Whitelisted Programs\033[0m")
    print(f"\033[1;36m{'─' * 55}\033[0m")

    if not programs:
        print("\n  \033[1;33m! Your whitelist is empty.\033[0m")
    else:
        print(f"\n  \033[90m{len(programs)} programs are currently whitelisted:\033[0m\n")

        for index, program in enumerate(programs, start=1):
            print(
                f"  \033[90m{index:02d}.\033[0m "
                f"\033[1;32m●\033[0m  {program}"
            )

    print(f"\n\033[1;36m{'─' * 55}\033[0m")
    print(f"  \033[90mTotal whitelisted:\033[0m \033[1;36m{len(programs)}\033[0m")
    print(f"\033[1;36m{'─' * 55}\033[0m")

    print("\n  \033[90mManage your whitelist:\033[0m")
    print("  \033[36m+\033[0m continuum whitelist add <program>")
    print("  \033[31m-\033[0m continuum whitelist remove <program>")
    print("  \033[36m→\033[0m continuum whitelist ls\n")

def whitelist_ls():
    programs = core.processes.get_all_processes_names()

    if not programs:
        print("No programs found.")
        return

    print("\n\033[1;36mContinuum | Available Programs\033[0m")
    print("\033[90mSelect programs to add to your whitelist.\033[0m\n")

    # Terminalbreite ermitteln
    terminal_width = shutil.get_terminal_size().columns
    col_width = 30
    columns = max(1, terminal_width // col_width)
    rows = (len(programs) + columns - 1) // columns

    for row in range(rows):
        line = ""

        for col in range(columns):
            index = row + col * rows

            if index < len(programs):
                name = programs[index]
                item = f"\033[36m{index + 1:>2}.\033[0m {name}"
                line += item + " " * max(1, col_width - len(name) - 4)

        print(line)

    print(f"\n\033[90m{len(programs)} programs found.\033[0m")
    print("\033[90mUse: continuum whitelist add <program>\033[0m\n")

def whitelist_add(program: str):
    if config.whitelist.add_allowed_program(program):
        print(f"\n  \033[1;32m✓ {program} added to whitelist.\033[0m\n")
    else:
        print(f"\n  \033[1;31m! {program} is already whitelisted.\033[0m\n")

def whitelist_remove(program: str):
    if config.whitelist.remove_allowed_program(program):
        print(f"\n  \033[1;32m✓ {program} removed from whitelist.\033[0m\n")
    else:
        print(f"\n  \033[1;31m! {program} is not whitelisted.\033[0m\n")
