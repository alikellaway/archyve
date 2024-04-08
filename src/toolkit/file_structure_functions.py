"""
Module contains functions useful for interacting with and manipulating file systems and structures.
"""
from sys import path as syspath
from typing import Generator
from itertools import chain
from random import randint
from pathlib import Path


def sub_files(directory: Path) -> Generator[Path, None, None]:
    """
    Returns a list of paths of the files in the given directory.
    :param directory: The directory in which to search.
    :return: The list of file paths in the given directory.
    """
    return (Path(f'{directory}') / f.name for f in directory.iterdir() if f.is_file())


def sub_dirs(directory: Path) -> Generator[Path, None, None]:
    """
    Returns a list of paths of the sub-folders to the given directory.
    :param directory: The string path of the folder from which to extract the paths of sub-folders from.
    :return: A list of sub folder paths.
    """
    return (Path(f'{directory}') / f.name for f in directory.iterdir() if f.is_dir())


def sub_paths(directory: Path | str) -> Generator[Path, None, None]:
    """
    Gets the resolved paths of every sub file in every sub folder into one list
    (all end points in the tree below the entry point given).
    :param directory: The root directory to get the tree of.
    :return: An iterable of string paths of each sub file.
    """
    directory: Path = Path(directory).resolve()
    sf = sub_files(directory)
    for d in sub_dirs(directory):
        sf = chain(sf, sub_paths(d))
    return sf


def create_test_directory(depth: int, location: Path | str = syspath[0], duplicate_percentage: int = 25,
                          max_directories: int = 5, max_files: int = 100):
    """
    Creates a random directory tree populated with text files. Some of which are duplicates.
    :param depth: The depth of the tree to create.
    :param location: The location in which to create the tree.
    :param duplicate_percentage: The percentage of the txt files that will be duplicates.
    :param max_directories: The maximum number of directories that can be created on each level of the tree.
    :param max_files: The maximum number of files that can be created on each level of the tree.
    :return:
    """
    if depth == 0:
        return

    location: Path = Path(location).resolve()

    # Create the directories in this level
    num_directories: int = randint(1, max_directories)
    for i in range(0, num_directories):
        (location / ("dir_" + str(i))).mkdir(exist_ok=True)

    # Populate this directory with some files that can be duplicates
    num_files = randint(1, max_files)
    dup_files = int(num_files * (duplicate_percentage / 100))
    unique_files = num_files - dup_files

    # Create the duplicate files
    for i in range(dup_files):
        path: Path = location / ('file_' + str(i) + '.txt')
        with open(path, 'w') as f:
            f.write("This is a randomly generated duplicate file.")

    # Create the unique files
    for i in range(dup_files, unique_files + dup_files):
        file_name = "file_" + str(i) + ".txt"
        with open(file_name, 'w') as f:
            f.write(
                f'This is a randomly generated unique file. Path hash: {hash(str(location) + file_name)}')
        path: Path = location / ('file_' + str(i) + '.txt')
        with open(path, 'w') as f:
            f.write(f'This is a randomly generated unique file. Path hash: {hash(str(path))}')

    # Do the same again for some of the directories we just created.
    for i in range(num_directories):
        create_test_directory(depth - 1, location=(location / f'dir_{i}'))
