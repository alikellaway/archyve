"""
Module contains logic to represent different kinds of media.

Author: ali.kellaway139@gmail.com
"""
from os.path import getsize, getctime
from PIL import Image, ExifTags
from functools import cache
from enum import Enum, auto
from pathlib import Path
from hashlib import md5


class MediaType(Enum):
    """
    An enumerator to represent different types of media.
    """
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
    TEXT = auto()
    UNKNOWN = auto()


class Media:
    """
    Media class is used to represent and assist in the management of files in a media library.
    """

    # Extension map is a map mapping of file extensions to the media type it pertains to
    EXTENSION_MAP: dict[str, MediaType] = {
        ".bmp": MediaType.IMAGE, ".cod": MediaType.IMAGE, ".gif": MediaType.IMAGE, ".ico": MediaType.IMAGE,
        ".ief": MediaType.IMAGE, ".jpe": MediaType.IMAGE, ".jpeg": MediaType.IMAGE, ".jpg": MediaType.IMAGE,
        ".pbm": MediaType.IMAGE, ".pgm": MediaType.IMAGE, ".png": MediaType.IMAGE, ".pnm": MediaType.IMAGE,
        ".ppm": MediaType.IMAGE, ".ras": MediaType.IMAGE, ".rgb": MediaType.IMAGE, ".svg": MediaType.IMAGE,
        ".tif": MediaType.IMAGE, ".tiff": MediaType.IMAGE, ".xbm": MediaType.IMAGE, ".xpm": MediaType.IMAGE,
        ".xwd": MediaType.IMAGE,

        ".3g2": MediaType.VIDEO, ".3gp": MediaType.VIDEO, ".avi": MediaType.VIDEO, ".flv": MediaType.VIDEO,
        ".h264": MediaType.VIDEO, ".m4v": MediaType.VIDEO, ".mkv": MediaType.VIDEO, ".mov": MediaType.VIDEO,
        ".mp4": MediaType.VIDEO, ".mpeg": MediaType.VIDEO, ".mpg": MediaType.VIDEO, ".rm": MediaType.VIDEO,
        ".swf": MediaType.VIDEO, ".vob": MediaType.VIDEO, ".wmv": MediaType.VIDEO,

        ".aif": MediaType.AUDIO, ".aifc": MediaType.AUDIO, ".aiff": MediaType.AUDIO, ".au": MediaType.AUDIO,
        ".flac": MediaType.AUDIO, ".m4a": MediaType.AUDIO, ".mp3": MediaType.AUDIO, ".ogg": MediaType.AUDIO,
        ".ra": MediaType.AUDIO, ".wav": MediaType.AUDIO, ".wma": MediaType.AUDIO,

        ".doc": MediaType.TEXT, ".docx": MediaType.TEXT, ".htm": MediaType.TEXT, ".html": MediaType.TEXT,
        ".odt": MediaType.TEXT, ".pdf": MediaType.TEXT, ".rtf": MediaType.TEXT, ".txt": MediaType.TEXT,
        ".wpd": MediaType.TEXT, ".wps": MediaType.TEXT, ".xml": MediaType.TEXT, ".xps": MediaType.TEXT
    }

    def __init__(self, path: Path | str):
        """
        Create a new instance of the class.
        :param path: The path file represent.
        """
        self.path: Path = Path(path)

    def __hash__(self) -> int:
        """
        Returns the hash of the underlying media file given its path.
        :return: A string hash of the file at the path.
        """
        md5_hasher = md5()
        with open(Path(self.path).resolve(), 'rb') as f:
            buf = f.read()
            md5_hasher.update(buf)
            return hash(md5_hasher.hexdigest())

    @property
    def m_type(self) -> MediaType:
        """
        Returns the media type enum of the given file if it is recognized, else Unknown.
        :return: The MediaType of the given path.
        """
        return Media.EXTENSION_MAP.get(Path(self.path).suffix, MediaType.UNKNOWN)

    @property
    def size(self) -> int:
        """
        Returns the size in bytes of the media file.
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
        Allows sorting of media objects by size.
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
        if not self.m_type == MediaType.IMAGE:
            return getctime(self.path)
        else:  # File is an image, look for the date it was taken.
            date_taken: float = self.exif.get('DateTimeOriginal')
            return date_taken if date_taken else getctime(self.path)

    @property
    def exif(self) -> dict | None:
        """
        Returns the exif data for the media if it's an image and has exif data. Else returns None.
        :return: The exif data for the image else None.s
        """
        if not self.m_type == MediaType.IMAGE:
            return None
        else:
            img = Image.open(self.path)
            return {ExifTags.TAGS[k]: v for k, v in img.getexif().items()}

    @staticmethod
    def is_media(path: Path | str) -> bool:
        """
        Returns whether the given file is a media file.
        :param path: The path of the file to check.
        :return:
        """
        return path.suffix in Media.__suffix_set

    @staticmethod
    @cache
    def __suffix_set():
        return set(Media.EXTENSION_MAP.keys())
