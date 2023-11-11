"""
Comparing files:
    + not based only on filename, rather on content
    + the comparison should be layered for performance
        1. is file length same?
        2. is hash same?
        3. use filecmp.cmp

    + The idea is to check for duplicates before a file is moved into both
    the target and dst.
    + This requires a dictionary whose key is file len,
    another one with the hashes
"""
from pathlib import Path
from random import choice
from pprint import pprint
import hashlib
import filecmp

src_folder = Path("../sample_dirs/media/")
extensions = ["*.txt", "*.md"]
dst_folder = Path("../sample_dirs/dst/target")

# building dicts for target
sizes = dict()
hashes = dict()
for tgt_file in dst_folder.glob("*"):
    tgt_file_size = tgt_file.stat().st_size
    if tgt_file_size not in sizes:
        sizes[tgt_file_size] = [tgt_file.name]
    else:
        sizes[tgt_file_size].append(tgt_file.name)
    with open(tgt_file, "rb") as file:
        tgt_file_md5 = hashlib.md5(file.read()).hexdigest()
        if tgt_file_md5 not in hashes:
            hashes[tgt_file_md5] = [tgt_file.name]
        else:
            hashes[tgt_file_md5].append(tgt_file.name)

pprint(sizes)
print("#" * 20)
pprint(hashes)

# Doing the comparison
filename_1, filename_2 = hashes["c8731f66f8f31b41e8bc00ca15f58797"]
file_1 = dst_folder / filename_1
file_2 = dst_folder / filename_2

is_identical = filecmp.cmp(file_1, file_2, shallow=False)
print(f"Are files equal?: {is_identical}")
