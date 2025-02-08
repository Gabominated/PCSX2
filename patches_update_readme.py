import os
import re

PATCHES_DIR = "patches"
README_FILE = os.path.join(PATCHES_DIR, "README.md")

def get_patch_info(patch_file):
    with open(patch_file, 'r') as file:
        content = file.read()
        match = re.search(r'gametitle=(.*?)\s.*?(\w{4}-\w{5})', content)
        if match:
            title = match.group(1).strip()
            serial = match.group(2).strip()
            return title, serial
        return None, None

def update_readme():
    patch_files = [f for f in os.listdir(PATCHES_DIR) if f.endswith('.pnach')]
    patches_info = []

    for patch_file in patch_files:
        title, serial = get_patch_info(os.path.join(PATCHES_DIR, patch_file))
        if title and serial:
            patches_info.append((title, serial, patch_file))

    patches_info.sort()

    with open(README_FILE, 'w') as readme:
        readme.write("# Parches para PCSX2\n\n")
        readme.write("Esta carpeta contiene parches para el emulador PCSX2. A continuación se presenta una lista de los parches disponibles:\n\n")
        for title, serial, patch_file in patches_info:
            readme.write(f"- [{title} {serial}]({patch_file})\n")

if __name__ == "__main__":
    update_readme()