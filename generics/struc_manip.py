"""
Module contains functions useful for interacting with and manipulating file systems and structures.
"""

import hashlib
import os
from sys import path as syspath


def files_equal(file1, file2):
    """
    Hashes the files at the given paths and returns whether they have equal content.
    :param file1: The location of one of the files in the comparison.
    :param file2: The location of the other file in the comparison.
    :return: boolean True if the files have equal contents.
    """
    return hash_from_path(file1) == hash_from_path(file2)


def hash_from_path(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        return hasher.hexdigest()


def get_file_size(filepath):
    """
    Returns the size of the file in bytes.
    :param filepath: The file's location.
    :return: int The size of the file in bytes.
    """
    return os.path.getsize(filepath)


def subfiles(directory: str) -> list[str]:
    """
    Returns a list of paths of the files in the given directory.
    :param directory: The directory in which to search.
    :return: The list of file paths in the given directory.
    """
    os.chdir(directory)
    return [f'{os.getcwd()}\\{f.name}' for f in os.scandir() if f.is_file()]


def subdirs(directory: str) -> list[str]:
    """
    Returns a list of paths of the sub-folders to the given directory.
    :param directory: The string path of the folder from which to extract the paths of sub-folders from.
    :return: A list of sub folder paths.
    """
    os.chdir(directory)
    return [f'{os.getcwd()}\\{f.name}' for f in os.scandir() if f.is_dir()]


def get_subpaths(directory: str) -> list[str]:
    """
    Use to get the paths of every sub file in every sub folder into one list.
    :param directory: The directory to recursively unpack.
    :return: A list of string paths of each sub file.
    """
    os.chdir(directory)
    sd = subdirs(directory)
    sf = subfiles(directory)
    if not not sd:  # if list not empty.
        for d in sd:
            sf += get_subpaths(d)
    return sf


def extension(path):
    """
    Retrieves a file's extension given its path or None if one is not found.
    :param path:
    :return:
    """
    try:
        return path.split(".")[1]
    except IndexError:
        return None


def name_from_path(path):
    """
    Returns a files name given its path.
    :param path: The file path.
    :return: The name of the file.
    """
    try:
        return path.split("\\")[-1]
    except IndexError:
        return None


def get_duplicates(direc_path):
    """
    Returns the paths of files that have equal content to another file in the directory. The first instance is not in
    the output.
    :param direc_path: The directory in which to search for duplicates.
    :return: A list of paths of files that are duplicates of another files.
    """
    paths = get_subpaths(direc_path)
    hashes = set()
    duplicates = []
    for path in paths:
        size = len(hashes)
        hashes.add(hash_from_path(path))
        if size < len(hashes):
            duplicates.append(path)
    return duplicates


def remove(paths):
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
            os.remove(p)
        except FileExistsError:
            failed.append(p)
            continue
    return failed


def remove_duplicates(directory):
    """
    Removes duplicate files from the given directory based on content.
    :param directory: The directory to check for duplicates.
    :return: A list of duplicates that failed to be removed.
    """
    return remove(get_duplicates(directory))


def create_test_directory(location=syspath[0], depth=3, filecount_max=10):
    for d in range(0, depth):
        os.mkdir(location)



if __name__ == '__main__':
    create_test_directory()

