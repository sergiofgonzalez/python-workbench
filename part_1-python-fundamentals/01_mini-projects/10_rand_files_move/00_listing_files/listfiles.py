"""
List files matching a certain filename patter from a dir,
non-recursively.
"""
from pathlib import Path
import glob

folder = Path("../sample_dirs/media")

# Listing specific extension
media_files = folder.glob("*.txt")
for media_file in media_files:
    print(f"Processing {media_file}")


# Listing all files
print("=" * 20)
media_files = folder.glob("*")
for media_file in media_files:
    print(f"Processing {media_file}")

# using `glob` to allow multiple extensions
print("=" * 20)
for media_file in glob.glob("*.txt", root_dir=folder) + glob.glob("*.md", root_dir=folder):
    print(f"Processing {media_file}")
