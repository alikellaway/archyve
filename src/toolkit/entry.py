"""
Module contains logic to represent different kinds of entries in an archive.

Author: ali.kellaway139@gmail.com
"""
from os.path import getsize, getctime
from PIL import Image, ExifTags
from functools import cache
from enum import Enum, auto
from pathlib import Path
from hashlib import md5


class EntryType(Enum):
    """
    An enumerator to represent different types of archive Entries.
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

    # Extension map is a map mapping of file extensions to the entry type it pertains to
    EXTENSION_MAP: dict[str, EntryType] = {
        ".bmp": EntryType.IMAGE, ".cod": EntryType.IMAGE, ".gif": EntryType.IMAGE, ".ico": EntryType.IMAGE,
        ".ief": EntryType.IMAGE, ".jpe": EntryType.IMAGE, ".jpeg": EntryType.IMAGE, ".jpg": EntryType.IMAGE,
        ".pbm": EntryType.IMAGE, ".pgm": EntryType.IMAGE, ".png": EntryType.IMAGE, ".pnm": EntryType.IMAGE,
        ".ppm": EntryType.IMAGE, ".ras": EntryType.IMAGE, ".rgb": EntryType.IMAGE, ".svg": EntryType.IMAGE,
        ".tif": EntryType.IMAGE, ".tiff": EntryType.IMAGE, ".xbm": EntryType.IMAGE, ".xpm": EntryType.IMAGE,
        ".xwd": EntryType.IMAGE,

        ".3g2": EntryType.VIDEO, ".3gp": EntryType.VIDEO, ".avi": EntryType.VIDEO, ".flv": EntryType.VIDEO,
        ".h264": EntryType.VIDEO, ".m4v": EntryType.VIDEO, ".mkv": EntryType.VIDEO, ".mov": EntryType.VIDEO,
        ".mp4": EntryType.VIDEO, ".mpeg": EntryType.VIDEO, ".mpg": EntryType.VIDEO, ".rm": EntryType.VIDEO,
        ".swf": EntryType.VIDEO, ".vob": EntryType.VIDEO, ".wmv": EntryType.VIDEO,

        ".aif": EntryType.AUDIO, ".aifc": EntryType.AUDIO, ".aiff": EntryType.AUDIO, ".au": EntryType.AUDIO,
        ".flac": EntryType.AUDIO, ".m4a": EntryType.AUDIO, ".mp3": EntryType.AUDIO, ".ogg": EntryType.AUDIO,
        ".ra": EntryType.AUDIO, ".wav": EntryType.AUDIO, ".wma": EntryType.AUDIO,

        ".doc": EntryType.TEXT, ".docx": EntryType.TEXT, ".htm": EntryType.TEXT, ".html": EntryType.TEXT,
        ".odt": EntryType.TEXT, ".pdf": EntryType.TEXT, ".rtf": EntryType.TEXT, ".txt": EntryType.TEXT,
        ".wpd": EntryType.TEXT, ".wps": EntryType.TEXT, ".xml": EntryType.TEXT, ".xps": EntryType.TEXT
    }

    def __init__(self, path: Path | str):
        """
        Create a new instance of the class.
        :param path: The path file represent.
        """
        self.path: Path = Path(path)

    def __hash__(self) -> int:
        """
        Returns the hash of the underlying file given its path.
        :return: A string hash of the file at the path.
        """
        md5_hasher = md5()
        with open(Path(self.path).resolve(), 'rb') as f:
            buf = f.read()
            md5_hasher.update(buf)
            return hash(md5_hasher.hexdigest())

    @property
    def m_type(self) -> EntryType:
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

    def __equal__(self, other) -> bool:
        """
        Returns whether the file's contents is equal to the other file's contents.
        :param other: The other file.
        :return: bool True if the contents are equal.
        """
        return self.__hash__() == other.__hash__()

    def __lt__(self, other) -> bool:
        """
        Allows sorting of Entry objects by size.
        :param other:
        :return:
        """
        return getsize(self.path) < getsize(other)

    @property
    def created(self):
        """
        Returns the creation date of the file (other the taken date in the item is an image and has an entry for this).
        :return:
        """
        if not self.m_type == EntryType.IMAGE:
            return getctime(self.path)
        else:  # File is an image, look for the date it was taken.
            date_taken: float = self.exif.get('DateTimeOriginal')
            return date_taken if date_taken else getctime(self.path)

    @property
    def exif(self) -> dict | None:
        """
        Returns the exif data for the entry if it's an image and has exif data. Else returns None.
        :return: The exif data for the image else None.s
        """
        if not self.m_type == EntryType.IMAGE:
            return None
        else:
            img = Image.open(self.path)
            return {ExifTags.TAGS[k]: v for k, v in img.getexif().items()}

    @staticmethod
    @cache
    def __suffix_set():
        return set(Entry.EXTENSION_MAP.keys())
