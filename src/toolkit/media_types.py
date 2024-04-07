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
    AUDIO = auto()
    VIDEO = auto()
    TEXT = auto()
    UNKNOWN = auto()


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
    ".3g2": MediaType.VIDEO,
    ".3gp": MediaType.VIDEO,
    ".avi": MediaType.VIDEO,
    ".flv": MediaType.VIDEO,
    ".h264": MediaType.VIDEO,
    ".m4v": MediaType.VIDEO,
    ".mkv": MediaType.VIDEO,
    ".mov": MediaType.VIDEO,
    ".mp4": MediaType.VIDEO,
    ".mpeg": MediaType.VIDEO,
    ".mpg": MediaType.VIDEO,
    ".rm": MediaType.VIDEO,
    ".swf": MediaType.VIDEO,
    ".vob": MediaType.VIDEO,
    ".wmv": MediaType.VIDEO,
    ".aif": MediaType.AUDIO,
    ".aifc": MediaType.AUDIO,
    ".aiff": MediaType.AUDIO,
    ".au": MediaType.AUDIO,
    ".flac": MediaType.AUDIO,
    ".m4a": MediaType.AUDIO,
    ".mp3": MediaType.AUDIO,
    ".ogg": MediaType.AUDIO,
    ".ra": MediaType.AUDIO,
    ".wav": MediaType.AUDIO,
    ".wma": MediaType.AUDIO,
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
    return SUFFIX_TO_MEDIATYPE_MAP.get(Path(path).suffix, MediaType.UNKNOWN)
