"""
Module contains functions useful for interacting with and manipulating file systems and structures.
"""

from hashlib import md5
from os import scandir, path as ospath, remove as osrmv, chdir, mkdir, listdir
from random import randint
from sys import path as syspath
from pathlib import Path
from typing import Iterable, Generator
from itertools import chain
from shutil import move


def files_equal(file1: Path | str, file2: Path | str) -> bool:
    """
    Hashes the files at the given paths and returns whether they have equal content.
    :param file1: The location of one of the files in the comparison.
    :param file2: The location of the other file in the comparison.
    :return: boolean True if the files have equal contents.
    """
    return hash_from_path(file1) == hash_from_path(file2)


def hash_from_path(path: Path | str) -> str:
    """ 
    Returns the hash of a file given its path.
    :param path: The path to the file to get the hash for.
    :return: A string hash of the file at the path.
    """
    hasher = md5()
    with open(path_handler(path).resolve(), 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        return hasher.hexdigest()


def subfiles(directory: Path | str) -> Generator:
    """
    Returns a list of paths of the files in the given directory.
    :param directory: The directory in which to search.
    :return: The list of file paths in the given directory.
    """
    direc = path_handler(directory).resolve()
    return (Path(f'{direc}') / f.name for f in scandir(direc) if f.is_file())


def subdirs(directory: Path | str) -> Generator:
    """
    Returns a list of paths of the sub-folders to the given directory.
    :param directory: The string path of the folder from which to extract the paths of sub-folders from.
    :return: A list of sub folder paths.
    """
    direc = path_handler(directory).resolve()
    return (Path(f'{direc}') / f.name for f in scandir(direc) if f.is_dir())


def subpaths(directory: Path | str) -> Generator:
    """
    Gets the resolved paths of every sub file in every sub folder into one list
    (all end points in the tree below the entry point given).
    :param directory: The root directory to get the tree of.
    :return: An iterable of string paths of each sub file.
    """
    direc = path_handler(directory)
    sf = subfiles(direc)
    for d in subdirs(direc):
        sf = chain(sf, subpaths(d))
    return sf


def get_duplicates(include: Path | Iterable[Path], exclude: Path | Iterable[Path] = None):
    """
    Returns a dictionary of file hashes mapped to a list of paths that have that hash (these paths are duplicate files).
    :param include: The list of paths to include in the search.
    :param exclude: The list of paths to exclude in the search.
    :return: A dictionary mapping file hashes to the paths that have files with that hash.
    """
    # Find the paths of all the files to check for duplicates.
    if isinstance(include, Path) or isinstance(include, str):  # One directory given
        paths = set(subpaths(include))
    elif isinstance(include, Iterable):  # Multiple directories given
        paths = {path for dir in include for path in subpaths(dir)}
    else:
        raise NotImplementedError

    # Find the paths of all the files to exclude from the search.
    if exclude is not None:
        if isinstance(exclude, str):
            exc = subpaths(exclude)
        elif isinstance(exclude, Iterable):
            exc = (path for dir in exclude for path in subpaths(dir))
        else:
            raise NotImplementedError
        # Remove all the excluded paths.
        for exc_path in exc:
            try:
                paths.remove(exc_path)
            except KeyError:
                continue

    hash_path_dict = {}  # A dictionary mapping file hash to the file path.
    for path in paths:
        try:
            hash_path_dict[hash := hash_from_path(path)].append(path)
        except KeyError:
            hash_path_dict[hash] = [path]

    # Filter through to find the hashes with multiple paths mapped (these are dup files).
    return dict(filter(lambda kvp: True if len(kvp[1]) > 1 else False, hash_path_dict.items()))


def remove(paths: Path | Iterable[Path]) -> list[Path]:
    """
    Removes the file at the given path, or multiple files from a list of paths.
    :param paths: A list of file paths to be removed.
    :return: failed A list of file paths that failed to be removed.
    """
    if isinstance(paths, Path):
        paths = tuple(paths)
    elif isinstance(paths, str):
        paths = tuple(path_handler(paths))
    failed = []  # A list of paths that failed to be removed.
    for p in paths:
        try:
            osrmv(p)
        except FileExistsError:
            failed.append(p)
            continue
    return failed


def remove_duplicates(directory: Path):
    """
    Removes duplicate files from the given directory based on content.
    :param directory: The directory to check for duplicates.
    :return: A list of duplicates that failed to be removed.
    """
    return remove(get_duplicates(directory))


def create_test_directory(depth, location=syspath[0], duplicate_percentage=25, max_directs=5, max_files=100):
    """
    Creates a random directory tree populated with text filese. Some of which are duplicates.
    :param depth: The depth of the tree to create.
    :param location: The location in which to create the tree.
    :param duplicate_percentage: The percentage of the txt files that will be duplicates.
    :param max_directs: The maximum number of directories that can be created on each level of the tree.
    :param max_files: The maximum number of files that can be created on each level of the tree.
    :return:
    """
    location = path_handler(location).resolve()
    if depth == 0:
        return
    chdir(location)
    num_direc = randint(1, max_directs)
    for i in range(0, num_direc + 1):
        dir_name = "dir_" + str(i)
        mkdir(dir_name)
    # Populate the direc with some files that can be duplicates
    num_files = randint(1, max_files)
    dup_files = int(num_files * (duplicate_percentage / 100))
    unique_files = num_files - dup_files
    # Create the dup files
    for i in range(dup_files):
        file_name = "file_" + str(i) + ".txt"
        with open(file_name, 'w') as f:
            f.write("This is a randomly generated duplicate file.")
    # Create the unique files
    for i in range(dup_files, unique_files + dup_files):
        file_name = "file_" + str(i) + ".txt"
        with open(file_name, 'w') as f:
            f.write(
                f'This is a randomly generated unique file. Path hash: {hash(str(location) + file_name)}')
    # Do the same again for some of the directories we just created.
    for i in range(num_direc):
        # 50% of the subdirectories will have subdirectories.
        if randint(0, 1) == 1:
            create_test_directory(
                depth - 1, location=ospath.join(location, f'dir_{i}'))


def path_handler(path: str | Path) -> Path:
    """
    Takes an input string or path and returns a path object allowing other functions to handle both strings and paths with only one line.
    :param path: The string or Path object.
    :return: A path object.
    """
    if isinstance(path, Path):
        return path
    if isinstance(path, str):
        return Path(path)
    raise NotImplementedError(
        f'Cannot convert object of type \'{type(path)}\' into a Path object.')


def safe_move(source_path: Path, dest_path: Path):
    """
    Move all files from source directory or a single file to destination directory. The process is safe, any clashing names will be renamed.
    :param source_path: The path of the file (or directory of files) to move to the destination path.
    :param dest_path: The path of the place to move the file(s).
    """
    def get_unique_path(dest_path: Path):
        """
        Returns a unique path to avoid overwriting existing files
        """
        if dest_path.is_file():
            base_name, extension = dest_path.stem, dest_path.suffix
            i = 1
            while True:
                new_name = f"{base_name}_{i}{extension}"
                new_path = dest_path.with_name(new_name)
                if not new_path.is_file():
                    return new_path
                i += 1
        else:
            return dest_path
    
    source_path = Path(source_path)
    dest_path = Path(dest_path)

    # Check if source_path is a file
    if source_path.is_file():
        # Move the file to the destination directory
        dest_path = get_unique_path(source_path, dest_path)
        move(str(source_path), str(dest_path))

    # Check if source_path is a directory
    elif source_path.is_dir():
        # Create the destination directory if it doesn't exist
        if not dest_path.exists():
            dest_path.mkdir(parents=True)

        # Move all files from the source directory to the destination directory
        for file_path in source_path.glob("*"):
            dest_file_path = dest_path / file_path.name

            # Move the file to the destination directory
            dest_file_path = get_unique_path(file_path, dest_file_path)
            move(str(file_path), str(dest_file_path))

    else:
        print(f"Error: {source_path} is not a file or a directory.")


if __name__ == '__main__':
    # import time

    # start_time = time.time()
    # # test_direc_path = "C:\\Users\\alike\\git\\media_tools\\test_direc"
    # pictures = f'D:\\Pictures'
    # # create_test_directory(5, test_direc_path)
    # dur = time.time() - start_time
    # pprint(dup)
    # print("--- %s seconds ---" % dur)
    print(list(subfiles("venv/Scripts")))
