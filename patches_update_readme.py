import os
import re

PATCHES_DIR = "PCSX2 Patches"
README_FILE = "README.md"

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

    # Ordenar la lista alfabéticamente por el título del juego
    patches_info.sort(key=lambda x: x[0])

    with open(README_FILE, 'w') as readme:
        readme.write("# PCSX2\n")
        readme.write("List of 50/60fps, widescreen and improvement patches for PCSX2 emulator\n\n")
        readme.write("| Name | Serial/Region | Details |\n")
        readme.write("| :--- | :---: | ---: |\n")
        for title, serial, patch_file in patches_info:
            patch_link = f"https://github.com/Gabominated/PCSX2/blob/main/PCSX2%20Patches/{patch_file}"
            readme.write(f"| {title} | [{serial}]({patch_link}) | |\n")

if __name__ == "__main__":
    update_readme()
