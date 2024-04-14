"""
This module contains functions useful for managing an archive of files. Whether that be checking equality, removing,
hashing or finding duplicates.

Author: ali.kellaway139@gmail.com
"""
from abc import ABC, abstractmethod
from types import TracebackType

from src.file_structure_functions import sub_paths
from typing import Generator, Iterable, Callable
from src.entry import Entry, EntryType
from pathlib import Path


class Archyve:

    def __init__(self, *directory: Path | str):
        """
        Initializes a new Archyve object.
        :param directory: The directory(s) that you want to many with this archyve object.
        """
        # Store the paths that will be managed by this archyve.
        self.paths: list[Path] = [Path(d) for d in directory]
        # Ensure all the given locations are directories and exist.
        for d in self.paths:
            if not d.is_dir():
                raise ValueError('Archyve can only accept directories in its constructor.')
            if not d.exists():
                raise FileNotFoundError(f'Non-existent directory: {str(d)}')

        # A space to keep a reference to the generator this Archyve will use
        self._entries: Generator[Entry] | None = None

    def archyve_from_generator(self, *generator: Generator[Entry, None, None]) -> 'Archyve':
        self.__init__(*list({sub_p.path.parent for p in generator for sub_p in p}))
        return self

    def entry_file_paths(self) -> Generator[Path, None, None]:
        """
        :return: Generator containing all files (regardless of depth) within all the folders within self.path.
        """
        return (sp for path in self.paths for sp in sub_paths(path))

    @property
    def entries(self) -> Generator[Entry, None, None]:
        """
        :return: Generator of Entry objects for all files under the Archyve's management.
        """
        if not self._entries:
            self._entries = (Entry(p) for p in self.entry_file_paths())

        return self._entries

    @entries.setter
    def entries(self, new_generator: Generator[Entry, None, None]) -> None:
        """
        Make the archyve iterate over a new set of entries.
        :param new_generator: The new generator of entries the archyve will iterate over.
        """
        self._entries = new_generator

    def duplicates(self, paths: Iterable[Path | Entry | str] | None = None,) -> list[list[Entry]]:
        """
        Returns a list of the paths of files that share the same md5 hash.
        :param paths: An iterable of paths in which to search for duplicates; defaults to all paths managed by the
                      archyve. You can filter the search space by inputting any series of paths or generators you like.
        :return: A dictionary mapping hashes to paths found in any of the parent directories or subdirectories that have
                 that hash.
        """
        search_space: Generator[Entry, None, None] = Archyve.create_entries(paths) if paths else self.entries
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
    def delete(*path: Path | str | Entry | Iterable[Path | str | Entry]) -> dict[Path, Exception] | None:
        """
        Removes files given their paths.
        :param path: The path or list of paths to remove.
        :return: A dictionary of the path mapped to the reason why it could not be removed.
        """
        # Make space for failures we might encounter
        failed: dict[Path, Exception] = {}

        # Attempt to delete all the files
        for entry in Archyve.create_entries(path):
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
                    yield from Archyve.create_entries(entry)
            else:
                raise NotImplementedError(f'We can\'t accept this object: \"{p.__repr__()}\"')

    @staticmethod
    def __filter_entries(generator: Generator[Entry, None, None], *entry_type: EntryType | str,
                         ) -> Generator[Entry, None, None]:
        """
        Returns a generator that yields only Entries of the given type.
        :param entry_type: The type of entry you want to be yielded by the generator.
        :param generator: The generator of entries to filter; defaults to the archyves self.entries() value.
        :return: A generator yielding only the type specified.
        """
        entry_type: list[EntryType] = [EntryType(e) if isinstance(e, str) else e for e in entry_type]
        return (e for e in filter(lambda e: e.entry_type in entry_type, generator))

    @property
    def images(self) -> 'Archyve':
        """
        :return: Self where entries are filtered to be images only.
        """
        return self.filter(lambda e: e.is_type(EntryType.IMAGE))

    @property
    def audios(self) -> 'Archyve':
        """
        :return: Self where entries are filtered to be audio only.
        """
        return self.filter(lambda e: e.is_type(EntryType.AUDIO))

    @property
    def videos(self) -> 'Archyve':
        """
        :return: Self where entries are filtered to be videos only.
        """
        return self.filter(lambda e: e.is_type(EntryType.VIDEO))

    @property
    def texts(self) -> 'Archyve':
        """
        :return: Self where entries are filtered to be text only.
        """
        return self.filter(lambda e: e.is_type(EntryType.TEXT))

    @property
    def unknowns(self) -> 'Archyve':
        """
        :return: Self where entries are filtered to be unknowns only.
        """
        return self.filter(lambda e: e.is_type(EntryType.UNKNOWN))

    def search(self, *string: str, any_all: Callable = any) -> Generator[Entry, None, None]:
        """
        Returns entries in the archyve whose paths contain any or all of the search strings.
        :param string: The string(s) that a path needs to contain to be 'found' as part of the search.
        :param any_all: Whether the path should contain all or any of the given strings.
        :return: A generator yielding paths that came up in the search.
        """
        return (e for e in self.entries if any_all(v in str(e.path) for v in string))

    def filter(self, func: Callable, inplace: bool = True) -> 'Archyve':
        """
        Returns the archyve filtered on your given function.
        :param func: The function to filter the archyve on (must return bool) (Trues are allowed through).
        :param inplace: Whether to return a new archyve or to return this one with the entries filtered.
        :return: This archyve but filtered on the given function.
        """
        filtered: Generator[Path, None, None] = (e for e in filter(func, self.entries))
        if inplace:
            self.entries = filtered
            return self
        else:
            new_archyve: Archyve = Archyve(*self.paths)
            new_archyve.entries = filtered
            return new_archyve
