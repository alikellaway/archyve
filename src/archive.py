"""
This module contains functions useful for managing an archive of files. Whether that be checking equality, removing,
hashing or finding duplicates.

Author: ali.kellaway139@gmail.com
"""
from src.file_structure_functions import sub_paths
from typing import Generator, Iterable, Callable
from src.entry import Entry, EntryType
from pathlib import Path


class Archive:

    def __init__(self, *directory: Path | str):
        """
        Initializes a new Archive object.
        :param directory: The directory(s) that you want to many with this archive object.
        """
        # Store the paths that will be managed by this archive.
        self.paths: list[Path | str] = [Path(d) for d in directory]
        # Ensure all the given locations are directories and exist.
        for d in self.paths:
            if not d.is_dir():
                raise ValueError('Archive can only accept directories in its constructor.')
            if not d.exists():
                raise FileNotFoundError(f'Non-existent directory: {str(d)}')

    def entry_file_paths(self) -> Generator[Path, None, None]:
        """
        :return: Generator containing all files (regardless of depth) within all the folders within self.path.
        """
        return (sp for path in self.paths for sp in sub_paths(path))

    @property
    def entries(self) -> Generator[Entry, None, None]:
        """
        :return: Generator of Entry objects for all files under the Archive's management.
        """
        return (Entry(p) for p in self.entry_file_paths())

    def duplicates(self, *paths: Path | str | Entry | Iterable[Path | Entry | str] | None) -> list[list[Entry]]:
        """
        Returns a list of the paths of files that share the same md5 hash.
        :param paths: An iterable of paths in which to search for duplicates; defaults to all paths managed by the
                      archive. You can filter the search space by inputting any series of paths or generators you like.
        :return: A dictionary mapping hashes to paths found in any of the parent directories or subdirectories that have
                 that hash.
        """
        search_space: Generator[Entry, None, None] = Archive.create_entries(paths) if paths else self.entries
        hashes_to_entries: dict[int, list[Entry]] = {}
        for entry in search_space:
            f_hash: int = hash(entry)
            duplicates: list[Path] | None = hashes_to_entries.get(f_hash)
            if duplicates:
                hashes_to_entries[f_hash].append(entry)
            else:
                hashes_to_entries[f_hash] = [entry]

        return [entries for entries in hashes_to_entries.values() if len(entries) > 1]

    @staticmethod
    def remove(*path: Path | str | Entry | Iterable[Path | str | Entry]) -> dict[Path, Exception] | None:
        """
        Removes files given their paths.
        :param path: The path or list of paths to remove.
        :return: A dictionary of the path mapped to the reason why it could not be removed.
        """
        # Make space for failures we might encounter
        failed: dict[Path, Exception] = {}

        # Attempt to delete all the files
        for entry in Archive.create_entries(path):
            result: Exception | None = entry.delete()
            if result:
                failed[entry.path] = result

        return failed if failed else None

    @staticmethod
    def create_entries(*path: Path | str | Entry | Iterable[Path | str | Entry]) -> Generator[Entry, None, None]:
        """
        Returns a generator of entries given an unpacked/packed Iterable of Path/str/Entry objects.
        :param path: The path/str/Entry (s) or Iterable of path/str/Entry (s) to return in the Entry Generator output.
        :return: A generator of entries.
        """
        for p in path:
            if isinstance(p, Path | str | Entry):
                yield Entry(p)
            elif isinstance(p, Iterable):
                for entry in p:
                    yield from Archive.create_entries(entry)
            else:
                raise NotImplementedError(f'We can\'t accept this object: \"{p.__repr__()}\"')

    @staticmethod
    def __filter_entries(entry_type: EntryType,
                         generator: Generator[Entry, None, None]) -> Generator[Entry, None, None]:
        """
        Returns a generator that yields only Entries of the given type.
        :param entry_type: The type of entry you want to be yielded by the generator.
        :param generator: The generator of entries to filter; defaults to the archives self.entries() value.
        :return: A generator yielding only the type specified.
        """
        return (e for e in filter(lambda e: e.entry_type == entry_type, generator))

    @property
    def images(self) -> Generator[Entry, None, None]:
        """
        :return: A generator of all the image entries in the Archive.
        """
        return Archive.__filter_entries(EntryType.IMAGE, self.entries)

    @property
    def audios(self) -> Generator[Entry, None, None]:
        """
        :return: A generator of all the audio entries in the Archive.
        """
        return Archive.__filter_entries(EntryType.AUDIO, self.entries)

    @property
    def videos(self) -> Generator[Entry, None, None]:
        """
        :return: A generator of all the video entries in the Archive.
        """
        return Archive.__filter_entries(EntryType.VIDEO, self.entries)

    @property
    def texts(self) -> Generator[Entry, None, None]:
        """
        :return: A generator of all the text entries in the Archive.
        """
        return Archive.__filter_entries(EntryType.TEXT, self.entries)

    @property
    def unknowns(self) -> Generator[Entry, None, None]:
        """
        :return: A generator of all the unknown entries in the Archive.
        """
        return Archive.__filter_entries(EntryType.UNKNOWN, self.entries)

    def search(self, *string: str, any_all: Callable = any) -> Generator[Entry, None, None]:
        """
        Returns entries in the archive whose paths contain any or all of the search strings.
        :param string: The string(s) that a path needs to contain to be 'found' as part of the search.
        :param any_all: Whether the path should contain all or any of the given strings.
        :return: A generator yielding paths that came up in the search.
        """
        return (e for e in self.entries if any_all(v in str(e.path) for v in string))
