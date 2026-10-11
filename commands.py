from config.whitelist import ALLOWED_PROGRAMS, BLACKLISTED_PROGRAMS
import core.processes
import core.launcher
import core.sessions

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
    processes = []
    tmp_int_negative = 0
    tmp_int_positive=0
    for pid in core.processes.get_all_processes():
        name=core.processes.get_process_name(pid)
        if name in ALLOWED_PROGRAMS and name not in BLACKLISTED_PROGRAMS:
            cwd=core.processes.get_process_cwd(pid)
            cmdline=core.processes.get_process_cmdline(pid)
            ppid=core.processes.get_parent_pid(pid)
            processes.append({"pid":pid,"name": name,"PPid":ppid,"cwd":cwd,"cmdline":cmdline})
            tmp_int_positive+=1
        else:
            tmp_int_negative+=1
    for i in processes:
        print(i)
    core.sessions.save_processes(processes)
    print(f"Session saved {tmp_int_positive} Processes and discarded {tmp_int_negative}")


def restore():
    core.launcher.launch_processes()

