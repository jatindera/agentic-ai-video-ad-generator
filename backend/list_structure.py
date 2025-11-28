import os

# Folders to exclude — you can add/remove as needed
EXCLUDE_DIRS = {'.venv', '__pycache__', '.git', '.idea', '.vscode', 'node_modules', 'tests', 'test*.py'}

OUTPUT_FILE = "project_structure.md"


def build_tree(start_path='.', indent_level=0):
    lines = []
    items = sorted(os.listdir(start_path))

    for i, item in enumerate(items):
        item_path = os.path.join(start_path, item)

        # Skip excluded dirs
        if os.path.isdir(item_path) and item in EXCLUDE_DIRS:
            continue

        # Markdown indentation using spaces
        prefix = "    " * indent_level

        # Tree connector
        connector = "├── " if i < len(items) - 1 else "└── "

        # Add folder/file entry
        lines.append(f"{prefix}{connector}{item}")

        # Recurse only for folders
        if os.path.isdir(item_path):
            lines.extend(build_tree(item_path, indent_level + 1))

    return lines


def generate_markdown(start_path='.'):
    tree_lines = build_tree(start_path)

    md_content = "# Project Folder Structure\n\n```\n" + "\n".join(tree_lines) + "\n```"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ Markdown file generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_markdown()
