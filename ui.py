# ui.py - All the pretty printing and input helpers live here
# Keeps other files clean. Reusable across the whole project.


def print_banner():
    """Prints the Eventra welcome banner."""
    print("=" * 50)
    print("        🎉  Welcome to Eventra  🎉")
    print("   Event Management and Ticketing System")
    print("=" * 50)


def print_line():
    """Prints a separator line."""
    print("-" * 50)


def print_success(msg):
    print(f"✅ {msg}")


def print_error(msg):
    print(f"❌ {msg}")


def print_info(msg):
    print(f"ℹ️  {msg}")


def get_int_input(prompt):
    """Safely gets an integer from the user. Returns None if invalid."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print_error("Please enter a valid number.")
        return None


def pause():
    """Waits for user to press Enter before continuing."""
    input("\nPress Enter to continue...")