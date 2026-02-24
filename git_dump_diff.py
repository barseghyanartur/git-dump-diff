#!/usr/bin/env python3
import subprocess
import sys

__title__ = "git-dump-diff"
__version__ = "0.1"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("main",)

LINE_WIDTH = 77
MAX_DEPTH = 10

STATUS_LABELS = {
    "A": "ADDED",
    "M": "UPDATED",
    "D": "REMOVED",
}

STATUS_COLORS = {
    "ADDED": "\033[1;32m",
    "UPDATED": "\033[1;33m",
    "REMOVED": "\033[1;31m",
}
RESET = "\033[0m"


def run_command(cmd):
    """Run a shell command and return its output, or None on failure."""
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        return None


def section_header(title):
    stars = "*" * LINE_WIDTH
    return f"# {stars}\n# {title}\n# {stars}"


def dashed_block(label):
    dashes = "-" * LINE_WIDTH
    return f"# {dashes}\n# {label}\n# {dashes}"


def get_changed_files(base, target):
    """Return dict of filename -> status label for all changed files."""
    raw = run_command(f"git diff --name-status -z {base}..{target}")
    if not raw:
        return {}

    result = {}
    parts = raw.split("\0")
    i = 0
    while i < len(parts):
        part = parts[i]
        if not part:
            i += 1
            continue
        status_char = part[0]
        if status_char == "R":
            # Rename: treat as REMOVED (old name) + UPDATED (new name)
            if i + 2 < len(parts):
                result[parts[i + 1]] = "REMOVED"
                result[parts[i + 2]] = "UPDATED"
            i += 3
        else:
            if i + 1 < len(parts):
                label = STATUS_LABELS.get(status_char, status_char)
                result[parts[i + 1]] = label
            i += 2
    return result


def build_tree_lines(root_name, changed_files):
    """Build tree-formatted lines from the set of affected file paths."""
    tree = {}
    for filepath in changed_files:
        node = tree
        for part in filepath.split("/"):
            node = node.setdefault(part, {})

    lines = [f"{root_name}/"]

    def render(node, prefix, path, depth):
        if depth >= MAX_DEPTH:
            return
        dirs = sorted((k for k in node if node[k]), key=str.lower)
        files = sorted((k for k in node if not node[k]), key=str.lower)
        items = dirs + files
        for idx, name in enumerate(items):
            is_last = idx == len(items) - 1
            connector = "└── " if is_last else "├── "
            child_prefix = prefix + ("    " if is_last else "│   ")
            full_path = f"{path}/{name}" if path else name
            if node[name]:  # directory
                lines.append(f"{prefix}{connector}{name}")
                render(node[name], child_prefix, full_path, depth + 1)
            else:  # file
                status = changed_files.get(full_path, "")
                annotation = f" ({status})" if status else ""
                lines.append(f"{prefix}{connector}{name}{annotation}")

    render(tree, "", "", 0)
    return lines


def is_binary(base, target, filename):
    cmd = f'git diff --numstat {base}..{target} -- "{filename}"'
    numstat = run_command(cmd)
    return bool(numstat and numstat.startswith("-"))


def print_tree_section(changed_files):
    root_raw = run_command("git rev-parse --show-toplevel")
    root_name = root_raw.split("/")[-1] if root_raw else "."

    print(section_header("Affected files structure"))
    print()
    print("Below is the layout of the project (to 10 levels), followed by the")
    print("contents of each key file.")
    print()
    print("Project directory layout")
    print()
    for line in build_tree_lines(root_name, changed_files):
        print(f"   {line}")
    print()


def print_changes_section(base, target, changed_files):
    print(section_header("Changes"))
    print()

    entries = sorted(changed_files.items())
    last_idx = len(entries) - 1
    for i, (filename, status) in enumerate(entries):
        color = STATUS_COLORS.get(status, "")
        status_display = f"{color}{status}{RESET}" if color else status
        print(dashed_block(f"Filename: {filename} ({status_display})"))
        print()

        if status != "REMOVED":
            if is_binary(base, target, filename):
                print("(Binary file - content skipped)")
            else:
                content = run_command(f'git show {target}:"{filename}"')
                print(content if content is not None else "(Empty file)")
            print()
            print(dashed_block(f"END '{filename}'"))
            print()

        if i < last_idx:
            print("\n ---- \n")
            print()


def main():
    if len(sys.argv) < 2:
        print(f"git-dump-diff v{__version__}")
        print("Usage: git dump-diff <base>..<target>")
        sys.exit(1)

    arg = sys.argv[1]

    if arg in ("--version", "-v"):
        print(f"git-dump-diff version {__version__}")
        sys.exit(0)

    if "..." in arg:
        base, target = arg.split("...", 1)
    elif ".." in arg:
        base, target = arg.split("..", 1)
    else:
        print("Error: Argument must be in format <base>..<target>")
        sys.exit(1)

    changed_files = get_changed_files(base, target)
    if not changed_files:
        print("No differences found.")
        return

    print_tree_section(changed_files)
    print_changes_section(base, target, changed_files)


if __name__ == "__main__":
    main()
