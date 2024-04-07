"""
Module contains logic to represent different kinds of media.

Author: ali.kellaway139@gmail.com
"""
from enum import Enum, auto
from pathlib import Path
from typing import Final


class MediaType(Enum):
    """
    An enumerator to represent different types of media.
    """
    IMAGE = auto()
    SOUND = auto()
    VIDEO = auto()
    TEXT = auto()
    OTHER = auto()


SUFFIX_TO_MEDIATYPE_MAP: Final[dict[str, MediaType]] = {
    ".bmp": MediaType.IMAGE,
    ".cod": MediaType.IMAGE,
    ".gif": MediaType.IMAGE,
    ".ico": MediaType.IMAGE,
    ".ief": MediaType.IMAGE,
    ".jpe": MediaType.IMAGE,
    ".jpeg": MediaType.IMAGE,
    ".jpg": MediaType.IMAGE,
    ".pbm": MediaType.IMAGE,
    ".pgm": MediaType.IMAGE,
    ".png": MediaType.IMAGE,
    ".pnm": MediaType.IMAGE,
    ".ppm": MediaType.IMAGE,
    ".ras": MediaType.IMAGE,
    ".rgb": MediaType.IMAGE,
    ".svg": MediaType.IMAGE,
    ".tif": MediaType.IMAGE,
    ".tiff": MediaType.IMAGE,
    ".xbm": MediaType.IMAGE,
    ".xpm": MediaType.IMAGE,
    ".xwd": MediaType.IMAGE,
    ".3g2": MediaType.SOUND,
    ".3gp": MediaType.SOUND,
    ".avi": MediaType.SOUND,
    ".flv": MediaType.SOUND,
    ".h264": MediaType.SOUND,
    ".m4v": MediaType.SOUND,
    ".mkv": MediaType.SOUND,
    ".mov": MediaType.SOUND,
    ".mp4": MediaType.SOUND,
    ".mpeg": MediaType.SOUND,
    ".mpg": MediaType.SOUND,
    ".rm": MediaType.SOUND,
    ".swf": MediaType.SOUND,
    ".vob": MediaType.SOUND,
    ".wmv": MediaType.SOUND,
    ".aif": MediaType.VIDEO,
    ".aifc": MediaType.VIDEO,
    ".aiff": MediaType.VIDEO,
    ".au": MediaType.VIDEO,
    ".flac": MediaType.VIDEO,
    ".m4a": MediaType.VIDEO,
    ".mp3": MediaType.VIDEO,
    ".ogg": MediaType.VIDEO,
    ".ra": MediaType.VIDEO,
    ".wav": MediaType.VIDEO,
    ".wma": MediaType.VIDEO,
    ".doc": MediaType.TEXT,
    ".docx": MediaType.TEXT,
    ".htm": MediaType.TEXT,
    ".html": MediaType.TEXT,
    ".odt": MediaType.TEXT,
    ".pdf": MediaType.TEXT,
    ".rtf": MediaType.TEXT,
    ".txt": MediaType.TEXT,
    ".wpd": MediaType.TEXT,
    ".wps": MediaType.TEXT,
    ".xml": MediaType.TEXT,
    ".xps": MediaType.TEXT,
}


def get_media_type_of(path: Path | str) -> MediaType:
    """
    Returns the media type enum of the given file if it is recognized, else Other.
    :param path: The path to get the media type of.
    :return: The MediaType of the given path.
    """
    return SUFFIX_TO_MEDIATYPE_MAP.get(Path(path).suffix, MediaType.OTHER)
