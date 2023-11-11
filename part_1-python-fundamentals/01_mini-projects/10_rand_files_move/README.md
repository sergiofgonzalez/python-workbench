# randfpck
> Picking random files from a folder and moving them to a destination

# Description

The idea of this tool is to automate the following scenario that I face whenever I'm preparing a bunch of media files (videos, photos, songs...) to be moved to a USB.

I have a source folder with large amount of (symbolic) links to media files, say `media/`. Nested within `media/` there's another folder say `already_used/` in which I move all the media files that I have already moved.

When I want to prepare a new batch of media files I manually execute the following actions:
1. Randomly select a media file from `media/`.
2. I copy it to a target directory, say `target_media/`.
3. When successfully copy I move the media file to `media/already_used/` so that it's not considered any further.
4. Rinse and repeat for a given number of times (say 10 times) so that I end up with 10 files on the `target_media/` folder.

## Error situations

+ Symbolic links tend to have names with spaces as in "Link to some_file.txt".

+ Sometimes, when executing #3 I get the error that the file has already been moved there.

    Ideally, when that happens I should check if the file contents are already the same. If so, I should just remove the symbolic link as it is already in the `media/already_used`. If it was only a name clash, I should just rename it and move it.

    Note that I don't care that much if there's a duplicate file with a different name.



## Possible Improvements

+ I would like to get a report of the total size of the files I have moved.

+ While having a CLI app is fine, it'd be cool to have a UI

## Breaking down the capabilities

+ [X] Listing files in directories with glob, the files might have multiple extensions (e.g., `.png`, `jpeg`, ...)
+ [X] Reading arguments from the command line
+ [X] Executing Python scripts from bash
+ [X] Following symlinks
+ [X] Choose randomly within a list, removing elements once chosen
+ [X] Comparing files by contents (using hash, maybe some other method).
+ [X] Data Model for the app (What state should I maintain and how?)
+ Dealing with errors:
    + file already there in either dst or seen
+ enabling @logtime to show how long a function has taken to execute.

## Data Model and App Logic

### App Logic

The application logic is simple (it is a CLI tool):

1. User invokes the script passing as argument:
    + Number of files to be copied
    + Src directory
    + Tgt directory
    + Seen directory (defaults to `{src}/seen`)
    + globbing patterns

2. System scans Src directory and creates a list of available files.

3. Until the number of files have been copied:
    1. Randomly choose a file, immediately remove it from the list of files.
    2. Compute its size and MD5
    3. Check if there's duplicate on Target. The check is based on both name and content (both are needed):
        + Filename check: there's a file on target with the same name as the one to be copied.
        + Content check: multilayered, if not same size, if not same MD5, if not filecmp.cmp equal, then files are different
        + if filename is duplicate but not content, suffix chosen file with `_[0-9]+` until no clashing.
        + if content is same log that info "duplicate on target" (into file log too), *don't remove the file* from the filesystem, (it has been removed from the chosen list). Then continue to next iteration.
    4. Check if there's duplicate on Seen:
        + Filename check
        + Content Check
        + if filename is duplicate but not content, suffix chosen file with `_[0-9]+` until no clashing.
        + if filename is duplicate but not content, suffix chosen file with `_[0-9]+` until no clashing.
        + if content is same log that info "duplicate on Seen" (into file log too), *don't remove the file* from the filesystem, (it has been removed from the chosen list). Then continue to next iteration.
    5. At this point no duplicates on Target or Seen:
        1. Copy file to Tgt
        2. Move file to Seen
        3. Log that information (to file too).
        4. Add file to list of copied files
        5. Update the Tgt and Seen data structures with the new file (as it should be considered in subsequent moves).

4. Present Report summary:
    + Number files scanned on Src
    + Number of files chosen (including dups)
    + Number of files copied
    + Size of files copied
    + List of files copied

### Data Model

Regarding the data model, there's not a lot of classes to design, as it's mostly a procedural script.

+ Parameters: use argparse globally
+ List of files in src (as returned by `glob.glob`)
+ ChosenFile &mdash; this can be a dataclass with parameters `file` (as returned by `glob.glob`), `size`, and `md5`, or handled directly while doing the iteration.
+ DirFiles &mdash; this can be a class holding the size and hash dictionaries for all the files in Target/Seen. It should also expose a method add so that the structures are updated one file is copied/moved.
+ ActivityTracker for the report.


### Manual Integration Tests

```bash
python randfpck.py --src ../int-tests-dir/media --dst ../int-tests-dir/dst/target/ --glob "*.txt" "*.md" --num-files 1
```

+ [X] num_files = 1, single file in src, empty tgt, empty seen
+ [X] num_files = 1, single file in src, no content or name clash, tgt with prev file, seen with prev file
+ [X] duplicate file (content)
+ [X] name clash (no dup content, but same size)

