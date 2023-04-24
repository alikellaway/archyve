"""
Module contains functions useful for interacting with and manipulating file systems and structures.
"""

from hashlib import md5
from os import scandir, path, remove as osrmv, chdir, mkdir
from random import randint
from sys import path as syspath
from pathlib import Path
from typing import Iterable


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
    with open(path_handler(path).resovle(), 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        return hasher.hexdigest()
    

def subfiles(directory: Path | str) -> list[Path]:
    """
    Returns a list of paths of the files in the given directory.
    :param directory: The directory in which to search.
    :return: The list of file paths in the given directory.
    """
    direc = path_handler(directory).resolve()
    return [Path(f'{direc}') / f.name for f in scandir(direc) if f.is_file()]


def subdirs(directory: Path | str) -> list[Path]:
    """
    Returns a list of paths of the sub-folders to the given directory.
    :param directory: The string path of the folder from which to extract the paths of sub-folders from.
    :return: A list of sub folder paths.
    """
    direc = path_handler(directory).resolve()
    return [Path(f'{direc}') / f.name for f in scandir(direc) if f.is_dir()]


def get_subpaths(directory: Path | str) -> list[Path]:
    """
    Use to get the paths of every sub file in every sub folder into one list.
    :param directory: The directory to recursively unpack.
    :return: A list of string paths of each sub file.
    """
    direc = path_handler(directory)
    sd = subdirs(direc)
    sf = subfiles(direc)
    if sd:  # if list not empty.
        for d in sd:
            sf += get_subpaths(d)
    return sf


def get_duplicates(include: str | Path | Iterable[Path] | Iterable[str], exclude: str | Path | Iterable[Path] = None) -> Iterable[Path]:
    """
    Returns the paths of files that have equal content to another file in the directory. The first instance is not in
    the output.
    :param exclude: A list of directories or files to exclude from the search.
    :param include: The directory or directories in which to start searching for duplicates.
    :return: A list of paths of files that are duplicates of another files.
    """
    # Change logic depending on whether the input is a single path of a list of paths.
    paths: Iterable[Path] = []
    if isinstance(include, Path):
        paths = get_subpaths(include)
    elif isinstance(include, list):
        for d in include:
            paths += get_subpaths(d)
    else:  # Not implemented
        raise NotImplementedError
    hashes = set()  # Use set to see if path is already seen
    duplicates = []  # List will store the paths of duplicate items (all the paths of each duplicate e.i. both photo 1 and photo 2)
    # Filter paths to exclude those in exclude list
    if exclude is not None:
        exc: Iterable[Path] = []
        if isinstance(exclude, str):
            exc.append(path_handler(exclude))
        elif isinstance(exclude, Iterable):
            exc += list(exclude)
        else:
            raise NotImplementedError
        for path in paths:
            for exclusion in exc:
                if path.resolve().find(exclusion.resolve()):
                    paths.remove(path)
    # Now comb for duplicates
    for path in paths:
        size = len(hashes)
        hashes.add(hash_from_path(path))
        if size < len(hashes):
            duplicates.append(path)
    return duplicates


def get_duplicates2(include: Path | Iterable[Path], exclude=None):
    print(f'Searching for duplicate files in:\n\t{include}')
    if isinstance(include, Path) or isinstance(include, str):  # One directory given
        paths = get_subpaths(include)
    elif isinstance(include, list):  # Multiple directories given
        paths = []
        for d in include:
            paths += get_subpaths(d)
    else:
        raise NotImplementedError
    if exclude is not None:
        print(f'Excluding directories and files under:')
        exc = []
        if isinstance(exclude, str):
            exc.append(exclude)
        elif isinstance(exclude, list):
            exc += exclude
        else:
            raise NotImplementedError
        for path in exc:
            print(f'\t{path}\n')
        for path in paths:
            for exclusion in exc:
                if path.commonpath([path, exclusion]):
                    paths.remove(path)

    hash_path_dict = {}
    for path in paths:
        file_hash = hash_from_path(path)
        if hash_path_dict.get(file_hash) is None:
            hash_path_dict[file_hash] = [path]
        else:
            hash_path_dict.get(file_hash).append(path)

    # Filter through to find the hashes with multiple paths mapped (these are dup files).
    rmv = []
    for key, value in hash_path_dict.items():
        if not len(value) > 1:
            rmv.append(key)
    for key in rmv:
        del hash_path_dict[key]
    return hash_path_dict


def remove(paths: Path | list[Path]) -> list[Path]:
    """
    Removes the file at the given path, or multiple files from a list of paths.
    :param paths: A list of file paths to be removed.
    :return: failed A list of file paths that failed to be removed.
    """
    if isinstance(paths, str):
        paths = [paths]
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
            f.write(f'This is a randomly generated unique file. Path hash: {hash(location + file_name)}')
    # Do the same again for some of the directories we just created.
    for i in range(num_direc):
        if randint(0, 1) == 1:  # 50% of the subdirectories will have subdirectories.
            create_test_directory(depth - 1, location=path.join(location, f'dir_{i}'))


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
    raise NotImplementedError(f'Cannot convert object of type \'{type(path)}\' into a Path object.')
    

if __name__ == '__main__':
    # import time

    # start_time = time.time()
    # # test_direc_path = "C:\\Users\\alike\\git\\media_tools\\test_direc"
    # pictures = f'D:\\Pictures'
    # # create_test_directory(5, test_direc_path)
    # dur = time.time() - start_time
    # pprint(dup)
    # print("--- %s seconds ---" % dur)
    print(subfiles("venv/Scripts"))
    l = [12,13]
    print(Path(l))