import sys


def clear_screen():
    """Clear the terminal without adding escape codes to redirected output."""
    if sys.stdout.isatty():
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
