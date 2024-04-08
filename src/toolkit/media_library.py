"""
This module contains functions useful for managing media. Whether that be checking equality, removing, hashing or
finding duplicates.

Author: ali.kellaway139@gmail.com
"""
from src.toolkit.file_structure_functions import sub_paths
from typing import Generator
from pathlib import Path
from media import Media


class MediaLibrary:

    def __init__(self, *directory: Path | str):
        self.path: list[Path | str] = list(directory)

    def media_file_paths(self) -> Generator[Path, None, None]:
        """
        Returns a generator of all the paths of all the files within all the folders (and their subfolders) in the
        MediaLibrary.path attribute.
        :return: Generator containing all files (regardless of depth) within all the paths within self.path.
        """
        return (sp for path in self.path for sp in sub_paths(path))

    def media(self) -> Generator[Media, None, None]:
        """
        A generator of Media objects for all files found in the directories managed by this library.
        :return: Generator of Media objects for all files under the libraries management.
        """
        return (Media(p) for p in self.media_file_paths())

    def duplicates(self) -> dict[int, list[Path]]:
        """
        Returns a dictionary of file hashes mapped to the paths of files that share that hash.
        :return: A dictionary mapping hashes to paths found in any of the parent directories or subdirectories that have
        that hash.
        """
        hashes_to_paths: dict[int, list[Path]] = {}

        for media in self.media():
            f_hash: int = hash(media)
            duplicates: list[Path] | None = hashes_to_paths.get(f_hash)
            if duplicates:
                hashes_to_paths[f_hash].append(media.path)
            else:
                hashes_to_paths[f_hash] = [media.path]

        return {file_hash: paths for file_hash, paths in hashes_to_paths.items() if len(paths) > 1}

    @staticmethod
    def remove(*path: Path | str) -> dict[Path, Exception]:
        """
        Removes files given their paths.
        :param path: The path or list of paths to remove.
        :return: A dictionary of the path mapped to the reason why it could not be removed.
        """
        failed: dict[Path, Exception] = {}
        for p in path:
            try:
                Path(p).unlink()
            except Exception as e:
                failed[p] = e

        return failed
