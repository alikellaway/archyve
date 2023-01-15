"""
Module contains functions useful for interacting with and manipulating file systems and structures.
"""

import hashlib
import os
import random
from sys import path as syspath
import shutil

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
    os.chdir(location)
    num_direc = random.randint(1, max_directs)
    for i in range(0, num_direc + 1):
        dir_name = "dir_" + str(i)
        os.mkdir(dir_name)
    # Populate the direc with some files that can be duplicates
    num_files = random.randint(1, max_files)
    dup_files = int(num_files * (duplicate_percentage / 100))
    unique_files = num_files - dup_files
    # Create the dup files
    for i in range(dup_files):
        file_name = "file_" + str(i) + ".txt"
        with open(file_name, 'w') as f:
            f.write("This is a randomly generated duplicate file.")
    # Create the unique files
    for i in range(unique_files):
        file_name = "file_" + str(i) + ".txt"
        with open(file_name, 'w') as f:
            f.write(f'This is a randomly generated unique file. Path hash: {hash(location + file_name)}')
    # Do the same again for some of the directories we just created.
    for i in range(num_direc):
        if random.randint(0, 1) == 1:  # 50% of the subdirectories will have subdirectories.
            create_test_directory(depth - 1, location=os.path.join(location, f'dir_{i}'))


def cut(filepath, destination, newname=None):
    os.chdir(syspath[0])
    src = filepath
    temp_folder_name = "cut_temp_folder"
    if newname is not None:
        os.mkdir(temp_folder_name)
        temp_path = f'{os.getcwd()}\\{temp_folder_name}'
        shutil.copy(filepath, temp_path)
        newpath = f'{temp_path}\\{newname}'
        os.rename(f'{temp_path}\\{name_from_path(filepath)}', newpath)
        src = newpath

    try:
        shutil.copy(src, destination)
        print(src)
        os.remove(filepath)
    except FileExistsError:
        raise FileExistsError
    except FileNotFoundError:
        raise FileNotFoundError
    finally:
        if newname is not None:
            # Delete the temp
            os.remove(src)
            os.rmdir(f'{syspath[0]}\\{temp_folder_name}')


if __name__ == '__main__':
    # test_direc_path = "/test_direc"
    # create_test_directory(5, test_direc_path)
    cut("cuttest.txt", "test_direc")
