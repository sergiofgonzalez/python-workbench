"""
Illustrates how copying and moving work when dealing with symlinks created
via `ln -s {existing file} {link name}`.
"""
from pathlib import Path
import shutil
import glob


# Copying files, following symlinks
src_folder = Path("../sample_dirs/media/")
extensions = ["*.txt", "*.md"]
dst_folder = Path("../sample_dirs/dst/target")

src_files_glob = []
for ext in extensions:
    src_files_glob.extend(glob.glob(ext, root_dir=src_folder))

for media_file in src_files_glob:
    src_file = src_folder / media_file
    dst_file = dst_folder / media_file
    shutil.copy(src_file, dst_file, follow_symlinks=True)
    print(f"{src_file} -> {dst_file}")

# Moving files (actual files, not symlinks)
mv_dst_folder = Path("../sample_dirs/media/seen")
for media_file in src_files_glob:
    src_file = src_folder / media_file
    mv_dst_file = mv_dst_folder / media_file
    src_file.rename(mv_dst_file)
    print(f"{src_file} -> {mv_dst_file}")
