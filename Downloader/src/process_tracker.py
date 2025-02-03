import sys,os


def print_progress_bar(completion_ratio):
    """Prints the progress bar to the console."""
    total_width=os.get_terminal_size().columns - 150
    filled_length = int(total_width * completion_ratio)
    bar = '=' * filled_length + '>' + ' ' * (total_width - filled_length)
    sys.stdout.write(f"\r(vscode) $[{bar}] {completion_ratio * 100:.2f}% complete")
    sys.stdout.flush()