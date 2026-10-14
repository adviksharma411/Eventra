import os
import time

LINE = "=" * 55


def print_banner(title):
    print()
    print(LINE)
    print(title.center(55))
    print(LINE)


def print_success(message):
    print(f"[OK] {message}")


def print_error(message):
    print(f"[ERROR] {message}")


def get_int_input(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":
            print_error("Input cannot be empty. Try again.")
            continue
        try:
            return int(value)
        except ValueError:
            print_error("Please enter a valid number.")


def get_yes_no(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print_error("Please enter y or n.")


def pause():
    input("\nPress Enter to continue...")


def clear_screen():
    time.sleep(0.3)
    os.system("cls" if os.name == "nt" else "clear")


def print_table(headers, rows):
    if not rows:
        print_error("No records found.")
        return

    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))

    for row in rows:
        print(" | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)))


if __name__ == "__main__":
    print_banner("UI TEST")
    print_success("This is a success message.")
    print_error("This is an error message.")
    print_table(
        ["ID", "Event", "City"],
        [(1, "Music Night", "Delhi"), (2, "Tech Fest", "Mumbai")]
    )
    pause()