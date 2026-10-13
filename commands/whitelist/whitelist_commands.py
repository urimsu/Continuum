import config.whitelist
import core.processes

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

def whitelist():
    programs = sorted(ALLOWED_PROGRAMS)

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"{CYAN}  CONTINUUM  |  Whitelisted Programs{RESET}")
    print(f"{CYAN}{'─' * 55}{RESET}")

    if not programs:
        print(f"\n  {YELLOW}! Your whitelist is empty.{RESET}")
    else:
        print(f"\n  {GRAY}{len(programs)} programs are currently whitelisted:{RESET}\n")

        for index, program in enumerate(programs, start=1):
            print(
                f"  {GRAY}{index:02d}.{RESET} "
                f"{GREEN}●{RESET}  {program}"
            )

    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"  {GRAY}Total whitelisted:{RESET} {CYAN}{len(programs)}{RESET}")
    print(f"{CYAN}{'─' * 55}{RESET}")

    print(f"\n  {GRAY}Manage your whitelist:{RESET}")
    print(f"  {BLUE}+{RESET} continuum whitelist add <program>")
    print(f"  {LIGHT_RED}-{RESET} continuum whitelist remove <program>")
    print(f"  {BLUE}→{RESET} continuum whitelist ls\n")


def whitelist_ls():
    programs = core.processes.get_all_processes_names()

    if not programs:
        print("No programs found.")
        return

    print(f"\n{CYAN}Continuum | Available Programs{RESET}")
    print(f"{GRAY}Select programs to add to your whitelist.{RESET}\n")

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
                item = f"{BLUE}{index + 1:>2}.{RESET} {name}"
                line += item + " " * max(1, col_width - len(name) - 4)

        print(line)

    print(f"\n{GRAY}{len(programs)} programs found.{RESET}")
    print(f"{GRAY}Use: continuum whitelist add <program>{RESET}\n")


def whitelist_add(program: str):
    if config.whitelist.add_allowed_program(program):
        print(f"\n  {GREEN}✓ {program} added to whitelist.{RESET}\n")
    else:
        print(f"\n  {RED}! {program} is already whitelisted.{RESET}\n")


def whitelist_remove(program: str):
    if config.whitelist.remove_allowed_program(program):
        print(f"\n  {GREEN}✓ {program} removed from whitelist.{RESET}\n")
    else:
        print(f"\n  {RED}! {program} is not whitelisted.{RESET}\n")

