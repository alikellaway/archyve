from file_structure_functions import subpaths
from typing import Generator
from pathlib import Path
from hashlib import md5


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
    with open(Path(path).resolve(), 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        return hasher.hexdigest()


def get_duplicates(*path: Path | str) -> dict[str, list[Path]]:
    """
    Searches recursively into the given directory(s) and returns a dictionary mapping file hashes to a list of Paths
    which all have that hash, i.e., the hash maps to files that are duplicates of each other.
    :param path: The path or list of paths to recursively search for duplicates in.
    :return: A dictionary mapping hashes to paths found in any of the parent directories or subdirectories that have
    that hash.
    """
    # Get a list of all end points in the directories given
    file_paths: Generator[Path, None, None] = (sp for directory in path for sp in subpaths(directory))

    # Construct a dictionary mapping hashes to paths that have that hash
    hashes_to_paths: dict[str, list[Path]] = {}

    for file_path in file_paths:
        # Get the file's hash
        file_hash = hash_from_path(file_path)
        entry: list[Path] | None = hashes_to_paths.get(file_hash)  # None if no entry
        if entry:
            entry.append(file_path)
        else:
            hashes_to_paths[file_hash] = [file_path]

    # Remove non-duplicate entries
    return {file_hash: duplicates for file_hash, duplicates in hashes_to_paths if len(duplicates) > 1}


def remove(*path: Path | str) -> dict[Path, Exception]:
    """
    Removes the file at the given path, or multiple files from a list of paths.
    :param path: The paths to remove
    :return: failed A list of file paths that failed to be removed.
    """
    failed: dict[Path, Exception] = {}  # A list of paths that failed to be removed.
    for p in path:
        try:
            Path(p).unlink(missing_ok=True)
        except Exception as exception:
            failed[p] = exception

    return failed
