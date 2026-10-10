from config.whitelist import ALLOWED_PROGRAMS, BLACKLISTED_PROGRAMS
import core.processes
import core.launcher


def list_sessions():
    print("liste anzeigen!")

def status():
    for pid in core.processes.get_all_processes():
        try:
            name=core.processes.get_process_name(pid)

            if name not in ALLOWED_PROGRAMS or name in BLACKLISTED_PROGRAMS:
                continue

            cwd=core.processes.get_process_cwd(pid)
            ppid= core.processes.get_parent_pid(pid)
            cmdline=core.processes.get_process_cmdline(pid)

            print(f"pid-({pid}) \n|| Name= {name} \n|| CWD= {cwd} \n|| PPID= {ppid} \n|| cmdline= {cmdline} \n")

        except (OSError, ProcessLookupError):
            continue

def save():
    print("Save current status")

def restore():
    for pid in core.processes.get_all_processes():
        name=core.processes.get_process_name(pid)
        cwd=core.processes.get_process_cwd(pid)
        core.launcher.launch_process(f"{name}", f"{cwd}")
