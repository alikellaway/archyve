from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import UnidentifiedImageError
from PIL import Image, ExifTags
from pathlib import Path


def get_image_exif_from_path(image_path: Path | str) -> dict:
    """
    Returns the exif data for the image at the given path.
    :param image_path: The path for the image to check.
    :return: A dictionary containing the exif data.
    """
    image: Image = Image.open(image_path, mode='r')
    try:
        return {
            ExifTags.TAGS[k]: v
            for k, v in image.getexif().items()
            if k in ExifTags.TAGS
        }
    finally:
        image.close()


def get_datetime_name(path: Path | str):
    """
    This function does its best to get the creation date of the media and then outputs that date concat with the
    original name.
    :param path: The path of the media of which to get the creation date.
    :return: str The name of the file but with its creation date at the front.
    """
    try:
        dt = get_image_exif_from_path(path).get('DateTime')
    except UnidentifiedImageError:  # Might have been a film
        try:
            dt = extractMetadata(createParser(path)).get('creation_date')
        except ValueError:  # Film had no creation_date attribute.
            dt = None

    if dt is None or dt == '':
        raise AttributeError('File has no DateTime entry in EXIF data.')

    return f'{str(dt).replace(":", "-")} {path.name}'


if __name__ == "__main__":
    print()
