from pathlib import Path
from enum import Enum, auto


class MediaType(Enum):
    IMAGE = auto()
    SOUND = auto()
    VIDEO = auto()
    TEXT = auto()
    OTHER = auto()


type_map = {
    MediaType.IMAGE: set(
        '.bmp',
        '.cod',
        '.gif',
        '.ico',
        '.ief',
        '.jpe',
        '.jpeg',
        '.jpg',
        '.pbm',
        '.pgm',
        '.png',
        '.pnm',
        '.ppm',
        '.ras',
        '.rgb',
        '.svg',
        '.tif',
        '.tiff',
        '.xbm',
        '.xpm',
        '.xwd'
    ),
    MediaType.SOUND: set(
        '.3g2',
        '.3gp',
        '.avi',
        '.flv',
        '.h264',
        '.m4v',
        '.mkv',
        '.mov',
        '.mp4',
        '.mpeg',
        '.mpg',
        '.rm',
        '.swf',
        '.vob',
        '.wmv'
    ),
    MediaType.VIDEO: set(
        '.aif',
        '.aifc',
        '.aiff',
        '.au',
        '.flac',
        '.m4a',
        '.mp3',
        '.ogg',
        '.ra',
        '.wav',
        '.wma'
    ),
    MediaType.TEXT: set(
        '.doc',
        '.docx',
        '.htm',
        '.html',
        '.odt',
        '.pdf',
        '.rtf',
        '.txt',
        '.wpd',
        '.wps',
        '.xml',
        '.xps'
    )
}


def ext_to_media(ext: str):
    """
    Given a file extension, this function will return an enum pertaining to what type of media it is.
    :param ext: The extension of the file to determine the media type of.
    :return: The type of the media.
    """
    for t in type_map.keys():
        if ext in type_map[t]:
            return t
    raise NotImplemented("This extension is not recognised as media.")
