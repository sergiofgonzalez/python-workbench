"""
Using choice to make a random selection on a list of files iteratively, removing
the selected file on every draw.
"""
from pathlib import Path
import glob
from random import choice


src_folder = Path("../sample_dirs/media/")
extensions = ["*.txt", "*.md"]
dst_folder = Path("../sample_dirs/dst/target")

src_files_glob = []
for ext in extensions:
    src_files_glob.extend(glob.glob(ext, root_dir=src_folder))

NUM_DRAWS = 15
print(f"num of files before: {len(src_files_glob)}")

for _ in range(0, min(NUM_DRAWS, len(src_files_glob))):
    selected_file = choice(src_files_glob)
    src_files_glob.remove(selected_file)
    print(f"Selected: {selected_file} (left: {len(src_files_glob)})")

print(f"num of files after: {len(src_files_glob)}")
if len(src_files_glob) == 0:
    print("Original file list exhausted")
