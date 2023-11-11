from pathlib import Path

class SomeClass:
    def __init__(self, folder) -> None:
        self.folder_path = Path(folder)
        self.files = ["file1"]

    def do_something_with_files(self):
        file = self.files[0]
        file_path = Path(self.folder_path) / file
        if file_path.is_dir():
            print(f"file_path {file_path} is a directory")
        else:
            print(f"file_path {file_path} is not a directory")
        if file_path.is_symlink():
            print(f"file_path {file_path} is a symbolyc link")
        else:
            print(f"file_path {file_path} is a not a symbolyc link")