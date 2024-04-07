"""
Module contains functions useful for interacting with and manipulating file systems and structures.
"""
from os import scandir, path as ospath, remove as osrmv, chdir, mkdir, listdir
from random import randint
from sys import path as syspath
from pathlib import Path
from typing import Generator
from itertools import chain
from shutil import move


def subfiles(directory: Path | str) -> Generator[Path, None, None]:
    """
    Returns a list of paths of the files in the given directory.
    :param directory: The directory in which to search.
    :return: The list of file paths in the given directory.
    """
    direc = path_handler(directory).resolve()
    return (Path(f'{direc}') / f.name for f in scandir(direc) if f.is_file())


def subdirs(directory: Path | str) -> Generator[Path, None, None]:
    """
    Returns a list of paths of the sub-folders to the given directory.
    :param directory: The string path of the folder from which to extract the paths of sub-folders from.
    :return: A list of sub folder paths.
    """
    direc = path_handler(directory).resolve()
    return (Path(f'{direc}') / f.name for f in scandir(direc) if f.is_dir())


def subpaths(directory: Path | str) -> Generator[Path, None, None]:
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
