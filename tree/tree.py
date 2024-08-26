import os
import time
import sys

ignore = [".git"]


def fix_colors() -> None:
    if not sys.stdout.isatty():
        for name in dir():
            if isinstance(name, str) and name[0] != "_":
                locals()[name] = ""
    else:
        if sys.platform == "win32":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32


colors = {
    "cyan": "\033[0;96m",
    "green": "\033[0;92m",
    "red": "\033[0;91m",
    "white": "\033[0;97m",
}


def get_ignored():
    try:
        with open(".gitignore", "r") as file:
            return [
                line.strip() for line in file.readlines() if not line.startswith("#")
            ] + ignore
    except FileNotFoundError:
        return ignore


def print_tree(directory, prefix: str = "", is_last: bool = True, output_file=None):
    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        return

    ignored = get_ignored()

    folders = sorted(
        [
            e
            for e in entries
            if os.path.isdir(os.path.join(directory, e)) and e not in ignored
        ]
    )
    files = sorted(
        [
            e
            for e in entries
            if os.path.isfile(os.path.join(directory, e)) and e not in ignored
        ]
    )

    entries = folders + files

    for i, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last_entry = i == len(entries) - 1

        if os.path.isdir(path):
            folder_icon = "┗ 📂" if is_last_entry else "┣ 📂"
            line = f"{prefix}{folder_icon}{entry}"
            if output_file:
                output_file.write(line + "\n")
            else:
                print(line)
            new_prefix = f"{prefix} " if is_last_entry else f"{prefix}┃ "
            print_tree(path, new_prefix, is_last_entry, output_file)
        else:
            file_icon = "┗ 📜" if is_last_entry else "┣ 📜"
            line = f"{prefix}{file_icon}{entry}"
            if output_file:
                output_file.write(line + "\n")
            else:
                print(line)


def main() -> None:
    start_time = time.time()
    sys.stdout.write(f"{colors['cyan']}• Generating Tree{colors['white']}")
    sys.stdout.flush()

    output_file_path = "directory_tree.txt"
    root_dir = os.getcwd()
    project_name = os.path.basename(root_dir)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(f"📦{project_name}\n")
        print_tree(root_dir, output_file=output_file)

    end_time = time.time()
    time_taken = end_time - start_time

    sys.stdout.write(
        f"\r{colors['green']}√ {colors['white']}Generated in {colors['cyan']}{time_taken:.2f}s{colors['white']} (saved to {colors['red']}{output_file_path}{colors['white']})\n"
    )
    sys.stdout.flush()


if __name__ == "__main__":
    main()
