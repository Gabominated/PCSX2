import os

# Define the paths
patches_folder = "PCSX2 Patches"
readme_path = "README.md"

# Function to generate the link for a given file
def generate_link(filename):
    game_title = filename.split('_')[0]  # Extract game title from filename
    serial = filename.split('_')[1].split('.')[0]  # Extract serial from filename
    link = f"[{serial}]({patches_folder}/{filename})"
    return game_title, link

# Read the existing README content
with open(readme_path, 'r') as file:
    readme_content = file.readlines()

# Find the table header in README
table_start = None
for i, line in enumerate(readme_content):
    if "| Game Title | Serial/Region | Details |" in line:
        table_start = i + 2  # Table starts after the header row
        break

if table_start is None:
    print("Table header not found in README.")
    exit()

# Generate the new lines for the table
new_lines = []
for filename in os.listdir(patches_folder):
    if filename.endswith(".pnach"):
        game_title, link = generate_link(filename)
        new_lines.append(f"| {game_title} | {link} |  |\n")

# Insert the new lines into the README content
readme_content[table_start:table_start] = new_lines

# Write the updated content back to README
with open(readme_path, 'w') as file:
    file.writelines(readme_content)

print("README.md updated successfully.")
