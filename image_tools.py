import os
import shutil
import PIL
from PIL import Image, ExifTags
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import struc_manip as sm


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
    except PIL.UnidentifiedImageError:  # Might have been a film
        try:
            dt = extractMetadata(createParser(path)).get('creation_date')
        except ValueError:  # Film had no creation_date attribute.
            dt = None

    if dt is None or dt == '':
        raise AttributeError
    return f'{str(dt).replace(":", "-")} {sm.name_from_path(path)}'


def copy_and_rename_file(file_path, new_name, destination_path):
    """
    Takes a file, copies it to a new location, and renames the file.
    :param file_path: The file to operate on.
    :param new_name: The new file name.
    :param destination_path: The destination of the file.
    :return:
    """
    shutil.copy(file_path, destination_path)
    original_name = file_path.split("\\")[-1]
    try:
        os.rename(f'{destination_path}\\{original_name}', f'{destination_path}\\{new_name}')
    except FileExistsError as e:
        os.remove(f'{destination_path}\\{original_name}')
        raise e

    # succeeded = False
    # while not succeeded:
    #     try:
    #         os.rename(f'{destination_path}\\{original_name}', f'{destination_path}\\{new_name}')
    #         succeeded = True
    #     except FileExistsError:  # If file exists, check if they're the same image.
    #         try:
    #             name_and_extension = new_name.split(".")
    #             new_name = name_and_extension[0] + "-dnt." + name_and_extension[1]
    #             os.rename(f'{destination_path}\\{original_name}', f'{destination_path}\\{new_name}')  # dnt: duplicate name token
    #             succeeded = True
    #         except FileExistsError:
    #             pass

if __name__ == "__main__":

    # proj_direc = os.getcwd()  # Need the project directory to create a file later.
    # paths = get_subpaths("D:\\Pictures\\Unsortables")  # Unpack all the paths in the folder.
    # failed_paths = []  # Create a space for paths that fail this process.
    # rename_dict = {}  # Create a space for the path re-mappings.
    #
    # for path in paths:
    #     try:  # Try to remap to begin with its date time.
    #         rename_dict[path] = get_datetime_name(path)
    #     except (AttributeError, PIL.UnidentifiedImageError):  # Fails as no DateTime attr or file type not accepted yet.
    #         failed_paths.append(path)
    #
    # # # # # Copy and rename all the photos to their new names # # # #
    # for p, rn in rename_dict.items():
    #     try:
    #         copy_and_rename_file(p, rn, "D:\\Pictures\\Sorteds")
    #         print(f'Copied and renamed {p} to {rn}')
    #     except FileExistsError:
    #         failed_paths.append(p)
    #         print(f'Failed {p}')
    #
    #
    # # # # Write the failed paths into a file. # # # #
    # os.chdir(proj_direc)
    # with open("failed_paths.txt", "w") as f:
    #     for p in failed_paths:
    #         f.write(f'{p}\n')
    # f.close()
    with open("duplicates.txt", 'r') as f:
        group_sizes = []
        group_size = 0
        for line in f:
            line = str(line)
            if line[0:5] == '-----':
                group_sizes.append(group_size)
                group_size = 0  # Skip the seperator lines
                continue
            group_size += 1
            infos = line.split('\t')
            print(infos)

            # path = infos[1]
            # print(path)

    # copy_and_rename_file("direc\\file.py", "f2.py", "direc\\subdirec1")