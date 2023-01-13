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


if __name__ == '__main__':
    print()