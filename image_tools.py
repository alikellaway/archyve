from PIL import UnidentifiedImageError
from PIL import Image, ExifTags
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import fsf as sm


def get_image_exif_from_path(image_path: str) -> dict[str: int]:
    """
    Returns the exif data for the image at the given path.
    :param image_path: The path for the image to check.
    :return: A dictionary containing the exif data.
    """
    image = Image.open(image_path, mode='r')
    try:
        return {
            ExifTags.TAGS[k]: v
            for k, v in image.getexif().items()
            if k in ExifTags.TAGS
        }
    finally:
        image.close()


def show_from_path(image_path):
    image = Image.open(image_path)
    image.show()


def get_datetime_name(path):
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
        raise AttributeError
    return f'{str(dt).replace(":", "-")} {sm.name_from_path(path)}'



if __name__ == "__main__":
    print()
