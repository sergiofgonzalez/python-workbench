"""
CLI tool that picks random file from a source directory, and copies them
to a target directory. Also, the tool moves them from the source to another
directory (used) so that they're no longer considered in future picks.
"""
import argparse
import filecmp
import glob
import hashlib
import logging
import shutil
from pathlib import Path
from random import choice
from typing import Optional, Sequence


def setup_logger() -> logging.Logger:
    """Sets up the logger for the CLI application. In the process a particular
    logging format is established, and a few handlers are added to the
    logger: a StreamHandler on stderr with a debug level, a file handler with
    a debug level so that everything is logged, and another file handler in
    which only errors and warnings are recorded for further inspection.

    Returns:
        logging.Logger: a completely configured Logger ready to use by the app.
    """
    logger = logging.getLogger(__name__)  # pylint: disable=redefined-outer-name
    logger.setLevel(logging.DEBUG)

    log_fmt_str = (
        "%(asctime)s.%(msecs)03d [%(levelname)8s] (%(name)s) | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        log_fmt_str, datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("randfpck.log")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(log_fmt_str, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    file_handler = logging.FileHandler("randfpck_err.log")
    file_handler.setLevel(logging.WARNING)
    file_formatter = logging.Formatter(log_fmt_str, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


def setup_arg_parser() -> argparse.ArgumentParser:
    """Sets up the ArgumentParser for the CLI application. It is configured
    with:

    + a basic description
    + a required argument for the source folder (`-s`/`--src`)
    + an optional argument for the used folder (`-u`/`--used`)
    + a required argument for the destination folder (`-d`/`--dst`)
    + a required argument for the globbing patterns (`-g`/`--glob`)
    + a required argument for the total number of files (`-n`/`--num-files`)


    Returns:
        argparse.ArgumentParser: a completely configured parser ready to use by
            the app.
    """
    parser = argparse.ArgumentParser(
        description=(
            "This program randomly picks files from a source folder "
            "and move them to a destination folder"
        )
    )
    parser.add_argument(
        "-s",
        "--src",
        metavar="{source folder}",
        required=True,
        help="Source folder from where to pick up files",
    )

    parser.add_argument(
        "-u",
        "--used",
        metavar="{used folder}",
        required=False,
        help="Folder where picked up files will be placed",
    )

    parser.add_argument(
        "-d",
        "--dst",
        metavar="{destination folder}",
        required=True,
        help="Destination folders where files will be moved",
    )

    parser.add_argument(
        "-g",
        "--glob",
        metavar="{globbing pattern}",
        nargs="+",
        required=True,
        help="Pattern indicating the files that will be picked up",
    )

    parser.add_argument(
        "-n",
        "--num-files",
        type=int,
        metavar="{number of files}",
        required=True,
        help="Number of files to be picked up",
    )

    return parser


class RandFilePickError(Exception):
    """Custom exception class for randfpck application related errors"""


class UserOptions:
    """Keeps track of the options used by the user.

    The object is instantiated with a Sequence[str] that results from having
    parsed the arguments passed by the user in the terminal.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, cli_args) -> None:
        self.logger.debug(
            "loading user options from CLI arguments: %s", cli_args
        )
        self.src_folder = Path(cli_args.src)
        self.dst_folder = Path(cli_args.dst)
        self.glob_filters = cli_args.glob
        if cli_args.used is not None:
            self.logger.debug("used folder was specified: %s", cli_args.used)
            self.used_folder = Path(cli_args.used)
        else:
            self.used_folder = self.src_folder / "seen"
            self.logger.debug(
                "used folder was not specified: used=%s", self.used_folder
            )
        self.num_files = cli_args.num_files

    def validate(self):
        """Checks that the corresponding folders exist and that
        the number of files is a positive number.
        """
        if not self.src_folder.exists():
            self.logger.error(
                "Source folder %s does not exist", self.src_folder
            )
            raise RandFilePickError(
                f"Source folder {self.src_folder} does not exist"
            )

        if not self.dst_folder.exists():
            self.logger.error(
                "Destination folder %s does not exist", self.dst_folder
            )
            raise RandFilePickError(
                f"Destination folder {self.dst_folder} does not exist"
            )

        if not self.used_folder.exists():
            self.logger.error("Used folder %s does not exist", self.used_folder)
            raise RandFilePickError(
                f"Destination folder {self.used_folder} does not exist"
            )

        if self.num_files < 1:
            self.logger.error(
                "Number of files should be a positive integer but was %d",
                self.num_files,
            )  # pylint: disable=line-too-long
            raise ValueError("Number of files must be a positive integer")

    def __str__(self):
        return f"src={self.src_folder}, patterns={self.glob_filters}, used={self.used_folder}, dst={self.dst_folder}, num_files={self.num_files}"  # pylint: disable=line-too-long

    def __repr__(self):
        return f"UserOptions(src_folder={self.src_folder}, dst_folder={self.dst_folder}, glob_filters={self.glob_filters}, used_folder={self.used_folder}, num_files={self.num_files})"  # pylint: disable=line-too-long


def find_files_matching(*, folder: Path, patterns: Sequence[str]) -> list[str]:
    """Scans the given directory in search of the files matching the given
    patterns.

    Args:
        folder (Path): the folder to be scanned
        patterns (Sequence[str]): a sequence of patterns to be matched against
            the files. Use ["*"] to return all the files.

    Returns:
        list[str]: a list of filenames found in the given folder whose name
            matches any of the given patterns.
    """
    if not folder or not patterns:
        raise ValueError(
            "find_files_matching require a folder and "
            "a non empty list of patterns"
        )

    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, root_dir=folder))
    return files


def file_path_for_filename(folder_path: Path, filename: str) -> Path:
    """Returns the file path given the path of the folder
    where the file sits and its name as string.

    Args:
        folder_path (Path): the Path of the folder where the file sits
        filename (str): the name of the file

    Returns:
        Path: the Path instance that represents the file
    """
    return folder_path / filename


def is_file(file_path: Path) -> bool:
    """Returns True if given file is not a directory or symbolic link

    Args:
        file_path (Path): the path to the file given

    Returns:
        bool: True if the given path corresponds to a regular file, False
            if the path given is a directory or symbolic link
    """
    if file_path.is_dir() or file_path.is_symlink():
        return False
    else:
        return True


def get_file_size(file_path: Path) -> Optional[int]:
    """Returns the file size in bytes for a regular file or None
    if the given file path corresponds to a directory or symbolic link

    Args:
        file_path (Path): the Path of the file whose size is wanted

    Returns:
        Optional[int]: the size of the file in bytes if the given path
            corresponds to a regular file, or None otherwise
    """
    if is_file(file_path):
        return file_path.stat().st_size
    else:
        return None


class FolderFiles:
    """A container for the files on a given folder"""

    logger = logging.getLogger(__name__)

    @staticmethod
    def get_file_md5(file) -> str:
        """Returns the MD5 hash for a given file

        Args:
            file: file descriptor or path

        Returns:
            the MD5 hash of the file as a string
        """
        with open(file, "rb") as f:  # pylint: disable=invalid-name
            file_md5 = hashlib.md5(f.read()).hexdigest()
        return file_md5

    def __init__(
        self,
        folder: Path | str,
        *,
        glob_patterns: Optional[list[str]] = None,
        build_metadata=False,
    ):
        """Container for the files in a given folder:

        Args:
            folder (Path | str): the folder that contains the files
            glob_patterns (list[str], optional): list of patterns describing the
                files to consider. Defaults to an empty list meaning all the
                files within the folder are considered.
            build_metadadata (boolean, optional): an optional flag indicating
                whether an associated metadata structure should be built for the
                files managed by this instance. Defaults to False meaning no
                metadata will be computed.

        Returns:
            A FolderFiles instance that includes a files attribute with the list
                of files tracked by the instance (the ones that match the list
                of globbing patterns) and a sizes dictionary which indexes all
                the files in the instance by size (that is, the key of the
                dictionary is the size, the value is the list of files with
                that size).
        """
        self.files = []
        self.folder = folder if isinstance(folder, Path) else Path(folder)
        self.glob_patterns = ["*"] if glob_patterns is None else glob_patterns
        self.files = find_files_matching(
            folder=self.folder, patterns=self.glob_patterns
        )
        if build_metadata:
            self.file_sizes = self._build_file_sizes_dict()
        else:
            self.file_sizes = dict()

    def _build_file_sizes_dict(self) -> dict[int, list[str]]:
        file_sizes: dict[int, list[str]] = dict()
        self.logger.info("Building metadata for %s folder", self.folder)
        for filename in self.files:
            file_path = file_path_for_filename(self.folder, filename)
            self.logger.debug(
                "About to compute metadata for file %s", file_path
            )
            if file_size := get_file_size(file_path):
                if file_size in file_sizes:
                    file_sizes[file_size].append(filename)
                else:
                    file_sizes[file_size] = [filename]
            else:
                self.logger.warning(
                    (
                        "Skipping metadata computation for %s: "
                        "it is either a directory or a symlink"
                    ),
                    file_path.name,
                )
        return file_sizes

    def __str__(self):
        newline_delim = "\n"
        return (
            f"folder={self.folder}, patterns={self.glob_patterns}, "
            f"files="
            f"{newline_delim.join(self.files) if self.files else self.files}, "
            f"file_sizes={self.file_sizes}"
        )

    def __repr__(self):
        return (
            f"FolderFiles(folder={self.folder}, "
            f"glob_patterns={self.glob_patterns}, "
            f"files={self.files}, file_sizes={self.file_sizes})"
        )


class ActivityTracker:
    """A class to hold the state of the process while running.

    The class is constructed with the number of files to be picked up and the
    source FolderFiles object that represents the Folder from where files are
    going to be picked, and the class will keep track of:
    - files_picked: the files that have been picked up
    - files_discarded: the files that have been discarded
    - src_folder_files: a reference to the FolderFiles object
    - orig_src_folder_size: the number of files originally in the FolderFiles
        object
    """

    logger = logging.getLogger(__name__)

    def __init__(
        self, num_files_to_pick: int, src_folder_files: FolderFiles
    ) -> None:
        if not isinstance(src_folder_files, FolderFiles):
            raise TypeError("src_folder_files must be a FolderFiles object")
        self.num_files_to_pick = num_files_to_pick
        self.files_picked = []
        self.files_discarded = []
        self.src_folder_files = src_folder_files
        self.orig_src_folder_size = len(src_folder_files.files)

    def process_done(self) -> bool:
        """Returns true is the process must be considered done based on the data
        tracked by this ActivityTracker object

        Returns:
            bool: True if the source folder has been emptied or if the requested
            number of files to be picked up have been picked up. False
            otherwise.
        """
        src_folder_exhausted = len(self.src_folder_files.files) == 0
        requested_files_picked = self.num_files_to_pick == len(
            self.files_picked
        )
        self.logger.debug(
            "src folder exhausted: %s, requested files picked: %s",
            src_folder_exhausted,
            requested_files_picked,
        )
        return src_folder_exhausted or requested_files_picked


def is_duplicate(file_path: Path, folder: FolderFiles) -> bool:
    """Checks whether the file identified by the given file path is a duplicate
    of an existing file of the given FolderFiles object.
    The strategy for checking the duplicates is multi-layered, where the more
    lightweight approach is executed first to be able to fail as early as
    possible: first, the size of the files are considered, then the MD5 hash of
    the file and finally a binary comparison is executed.

    Args:
        file_path (Path): the path to the file to whose potential duplicates are
            to be found.
        folder (FolderFiles): the container of files that will be matched
            against the given file.

    Returns:
        bool: True if a duplicate is found, False otherwise.
    """
    file_size = file_path.stat().st_size
    if file_size in folder.file_sizes:
        logger.warning(
            "found a hit for file %s (size %d) in folder %s: will compute MD5",
            file_path,
            file_size,
            folder.folder,
        )
        file_md5 = FolderFiles.get_file_md5(file_path)
        for f in folder.file_sizes[file_size]:
            f_path = file_path_for_filename(folder.folder, f)
            f_md5 = FolderFiles.get_file_md5(f_path)
            if file_md5 == f_md5:
                logger.warning(
                    (
                        "found a hit for file %s (hash %s) in folder %s: "
                        "will compare files"
                    ),
                    file_path,
                    file_md5,
                    folder.folder,
                )  # pylint: disable=line-too-long
                is_identical = filecmp.cmp(file_path, f_path, shallow=False)
                if is_identical:
                    logger.warning("%s and %s are identical", file_path, f_path)
                    return True

    logger.debug(
        "No duplicates found for file %s on %s", file_path, folder.folder
    )
    return False


def get_unique_filename(file_path: Path, folders_to_check: list[Path]) -> str:
    """Returns a filename that does not clash with the ones found in the given
    folders to check

    Args:
        file_path (Path): the path of the file whose name is to be checked
            against the ones in folders_to_check
        folders_to_check (list[Path]): list of Paths

    Returns:
        str: a new name for the given file so that its name doesn't clash with
            any of the names given in the folders_to_check argument.
    """
    # The algorithm can be clearly improved and also makes the code difficult
    # to test - I've kept it to illustrate how contrived the test mocks can get.
    filename = file_path.name

    found_unique = False
    seq_no = 0
    while not found_unique:
        exist_in_any = any(
            [
                file_path_for_filename(folder, filename).exists()
                for folder in folders_to_check
            ]
        )
        if exist_in_any:
            seq_no += 1
            filename = f"{file_path.stem}.{seq_no}{file_path.suffix}"
        else:
            found_unique = True

    return filename


def load_user_options() -> UserOptions:
    """Reads the information given by the user and returns an instance of
    UserOptions that contains a structured representation of such information.
    In the process, the options provided by the user are validated, so in case
    of failure, this function may raise a ValueError or RandFilePickError
    exception.


    Returns:
        UserOptions: a UserOptions instance that contains the information given
            by the user.
    """
    arg_parser = setup_arg_parser()
    args = arg_parser.parse_args()

    result = UserOptions(args)
    logger.debug("user options loaded: %s", result)

    result.validate()
    logger.debug("user options validated: %s", result)
    return result


def print_report(at: ActivityTracker) -> None:
    """Prints a report with certain information about how the process was
    carried out.
    """
    print(
        f"""{'#' * 50}
Number of files to pick up: {at.num_files_to_pick:>5}
Number of files scanned   : {at.orig_src_folder_size:>5}
Number of files moved     : {len(at.files_picked):>5}
Number of files discarded : {len(at.files_discarded):>5}
"""
    )


logger = (
    setup_logger()
)  # TODO this should be moved to the beginning of the file


if __name__ == "__main__":
    logger.info("starting execution")

    user_options = load_user_options()

    src_folder = FolderFiles(
        user_options.src_folder, glob_patterns=user_options.glob_filters
    )
    logger.debug("src files scanned: %s", src_folder)

    dst_folder = FolderFiles(user_options.dst_folder, build_metadata=True)
    logger.debug("dst files scanned: %s", dst_folder)

    used_folder = FolderFiles(user_options.used_folder, build_metadata=True)
    logger.debug("used files scanned: %s", used_folder)

    activity_tracker = ActivityTracker(user_options.num_files, src_folder)
    logger.debug("initializing process: %s", activity_tracker)

    while not activity_tracker.process_done():
        selected_file_str = choice(activity_tracker.src_folder_files.files)
        activity_tracker.src_folder_files.files.remove(selected_file_str)
        selected_file_path = Path(user_options.src_folder) / selected_file_str

        logger.debug(
            "about to check for duplicates of file %s in %s",
            selected_file_path,
            user_options.dst_folder,
        )  # pylint: disable=line-too-long
        if is_duplicate(selected_file_path, dst_folder):
            activity_tracker.files_discarded.append(selected_file_path)
            continue

        logger.debug(
            "about to check for duplicates of file %s in %s",
            selected_file_path,
            user_options.used_folder,
        )  # pylint: disable=line-too-long
        if is_duplicate(selected_file_path, used_folder):
            activity_tracker.files_discarded.append(selected_file_path)
            continue

        logger.info("File %s has been found to be unique", selected_file_path)

        logger.debug(
            (
                "about to choose unique name for file %s "
                "to prevent clashes in %s and %s"
            ),
            selected_file_path,
            user_options.dst_folder,
            user_options.used_folder,
        )
        final_filename = get_unique_filename(
            selected_file_path,
            [user_options.dst_folder, user_options.used_folder],
        )

        # Copy file to dst
        dst_file = Path(dst_folder.folder) / final_filename
        shutil.copy(selected_file_path, dst_file, follow_symlinks=True)
        logger.info("%s copied to %s", selected_file_path, dst_file)

        # Move file to seen
        used_file = Path(used_folder.folder) / final_filename
        selected_file_path.rename(used_file)
        logger.info("%s moved to %s", selected_file_path, used_file)

        activity_tracker.files_picked.append(selected_file_path)

    print_report(activity_tracker)
    logger.info("Process completed")
