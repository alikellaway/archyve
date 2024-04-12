"""
Module contains classes to represent different kinds of files in an archive.

NB: Each file in an archive is an Entry.

Author: ali.kellaway139@gmail.com
"""
from PIL import Image, ExifTags, UnidentifiedImageError
from os.path import getsize, getctime
from datetime import datetime
from typing import Any, Union
from functools import cache
from enum import Enum, auto
from pathlib import Path
from hashlib import md5


class EntryType(Enum):
    """
    An enumerator to represent different types of files within an archive. Each file in an archive is an Entry.
    """
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
    TEXT = auto()
    UNKNOWN = auto()


class Entry:
    """
    Class is used to represent and assist in the management of files in an archive.
    """

    # Mapping of file extensions to EntryType
    EXTENSION_MAP: dict[str, EntryType] = {
        ".bmp": EntryType.IMAGE, ".cod": EntryType.IMAGE, ".gif": EntryType.IMAGE, ".ico": EntryType.IMAGE,
        ".ief": EntryType.IMAGE, ".jpe": EntryType.IMAGE, ".jpeg": EntryType.IMAGE, ".jpg": EntryType.IMAGE,
        ".pbm": EntryType.IMAGE, ".pgm": EntryType.IMAGE, ".png": EntryType.IMAGE, ".pnm": EntryType.IMAGE,
        ".ppm": EntryType.IMAGE, ".ras": EntryType.IMAGE, ".rgb": EntryType.IMAGE, ".svg": EntryType.IMAGE,
        ".tif": EntryType.IMAGE, ".tiff": EntryType.IMAGE, ".xbm": EntryType.IMAGE, ".xpm": EntryType.IMAGE,
        ".xwd": EntryType.IMAGE,  # Add any extra image extensions here

        ".3g2": EntryType.VIDEO, ".3gp": EntryType.VIDEO, ".avi": EntryType.VIDEO, ".flv": EntryType.VIDEO,
        ".h264": EntryType.VIDEO, ".m4v": EntryType.VIDEO, ".mkv": EntryType.VIDEO, ".mov": EntryType.VIDEO,
        ".mp4": EntryType.VIDEO, ".mpeg": EntryType.VIDEO, ".mpg": EntryType.VIDEO, ".rm": EntryType.VIDEO,
        ".swf": EntryType.VIDEO, ".vob": EntryType.VIDEO, ".wmv": EntryType.VIDEO,  # Add video extensions here

        ".aif": EntryType.AUDIO, ".aifc": EntryType.AUDIO, ".aiff": EntryType.AUDIO, ".au": EntryType.AUDIO,
        ".flac": EntryType.AUDIO, ".m4a": EntryType.AUDIO, ".mp3": EntryType.AUDIO, ".ogg": EntryType.AUDIO,
        ".ra": EntryType.AUDIO, ".wav": EntryType.AUDIO, ".wma": EntryType.AUDIO,  # Add audio extensions here

        ".doc": EntryType.TEXT, ".docx": EntryType.TEXT, ".htm": EntryType.TEXT, ".html": EntryType.TEXT,
        ".odt": EntryType.TEXT, ".pdf": EntryType.TEXT, ".rtf": EntryType.TEXT, ".txt": EntryType.TEXT,
        ".wpd": EntryType.TEXT, ".wps": EntryType.TEXT, ".xml": EntryType.TEXT, ".xps": EntryType.TEXT
        # Add any extra text extensions here
    }

    def __init__(self, path: Union[Path, str, 'Entry']):
        """
        Create a new instance of the class.
        :param path: The path of the file to represent.
        """
        # Use our parameters to create the object.
        if isinstance(path, Path | str):
            self.path: Path = Path(path)

        # If we got an Entry object as input
        elif isinstance(path, Entry):
            for attribute, value in path.__dict__.items():
                setattr(self, attribute, value)

        # We don't know what to do with this input type
        else:
            raise NotImplementedError(f'Constructor for entry with input \"{path}\" not implemented.')

    def __hash__(self) -> int:
        """
        Returns the hash of the underlying file given its path.
        :return: A string hash of the file at the path.
        """
        md5_hash = md5()
        with open(Path(self.path).resolve(), 'rb') as f:
            buf = f.read()
            md5_hash.update(buf)
            return hash(md5_hash.hexdigest())

    @property
    def entry_type(self) -> EntryType:
        """
        Returns the entry type enum of the given file if it is recognized, else Unknown.
        :return: The EntryType of the given path.
        """
        return Entry.EXTENSION_MAP.get(Path(self.path).suffix, EntryType.UNKNOWN)

    @property
    def size(self) -> int:
        """
        Returns the size in bytes of the file.
        :return:
        """
        return getsize(self.path)

    def __eq__(self, other: Any) -> bool:
        """
        Returns whether the file's contents is equal to the other file's contents.
        :param other: The other file.
        :return: bool True if the contents are equal.
        """
        return isinstance(other, Entry) and hash(self) == hash(other)

    def __lt__(self, other: Any) -> bool:
        """
        Allows sorting of Entry objects by file size.
        :param other: The other item to compare size with
        :return:
        """
        if not isinstance(other, Entry):
            raise NotImplementedError(f'Size comparison between Entry and \"{type(other)}\" is not implemented.')
        return getsize(self.path) < getsize(other.path)

    @property
    def created(self) -> datetime:
        """
        :return: The creation date of the file (other the taken date in the item is an image and has an entry for this).
        """
        if not self.entry_type == EntryType.IMAGE:
            time_stamp: float = getctime(self.path)
        else:  # File is an image, look for the date it was taken.
            exif: dict | None = self.exif
            date_taken: str | None = exif.get('DateTimeOriginal') if exif else None
            time_stamp: float = float(date_taken) if date_taken else getctime(self.path)

        return datetime.fromtimestamp(time_stamp)

    @property
    def exif(self) -> dict[str, str] | None:
        """
        :return: the exif data for the entry if it's an image and has exif data. Else returns None.
        """
        if not self.entry_type == EntryType.IMAGE:
            return None
        else:
            try:
                with Image.open(self.path) as img:
                    return {ExifTags.TAGS[k]: v for k, v in img.getexif().items()}
            except UnidentifiedImageError:
                return None

    @staticmethod
    @cache
    def __suffix_set():
        """
        :return: A set of all the suffixes known.
        """
        return set(Entry.EXTENSION_MAP.keys())

    def __repr__(self):
        """
        :return: A string representation of the entry (its path).
        """
        return str(self.path)

    def delete(self) -> Exception | None:
        """
        Deletes the entry (actually deletes the underlying file; be careful).
        :return: boolean describing whether the deletion was successful (true if delete successful).
        """
        try:
            self.path.unlink()
        except Exception as e:
            return e
