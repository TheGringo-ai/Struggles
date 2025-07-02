import os
from pathlib import Path

# Define common env folder names
env_names = [".venv", "venv", "env", ".env"]

# Define ignored paths to avoid deleting critical or system files
ignored_keywords = [
    "node_modules", "CloudStorage", "Trash", ".vscode", ".rustup", ".rbenv", ".pyenv"
]

def is_safe_to_delete(path):
    return not any(keyword in str(path) for keyword in ignored_keywords)

def find_and_delete_envs(base_path):
    print(f"🔍 Scanning for environments under {base_path}...\n")
    deleted = []
    for root, dirs, _ in os.walk(base_path):
        for d in dirs:
            if d in env_names:
                full_path = Path(root) / d
                if is_safe_to_delete(full_path):
                    print(f"🗑️ Deleting: {full_path}")
                    try:
                        os.system(f'rm -rf "{full_path}"')
                        deleted.append(str(full_path))
                    except Exception as e:
                        print(f"❌ Error deleting {full_path}: {e}")
    return deleted

if __name__ == "__main__":
    home = str(Path.home())
    deleted_envs = find_and_delete_envs(home)
    print(f"\n✅ Done. {len(deleted_envs)} environment(s) removed.")