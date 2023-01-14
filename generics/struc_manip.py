"""
Module contains functions useful for interacting with and manipulating file systems and structures.
"""

import hashlib
import os


def files_equal(file1, file2):
    """
    Hashes the files at the given paths and returns whether they have equal content.
    :param file1: The location of one of the files in the comparison.
    :param file2: The location of the other file in the comparison.
    :return: boolean True if the files have equal contents.
    """
    hasher = hashlib.md5()
    with open(file1, 'rb') as f1:
        buf = f1.read()
        hasher.update(buf)
        file1_hash = hasher.hexdigest()
    with open(file2, 'rb') as f2:
        buf = f2.read()
        hasher.update(buf)
        file2_hash = hasher.hexdigest()
    return file1_hash == file2_hash


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


if __name__ == '__main__':
    print(extension(""))