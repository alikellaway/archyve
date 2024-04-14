"""
Script contains logic to analyse and clean an image library. The goal is to remove duplicates, keeping the oldest
copy that we can find. We also want to flatten the entire library, so that the user can sort by date manually and drag
into albums.

Author: ali.kellaway139@gmail.com
"""
from archyve import Archyve
from archyve.entry import Entry


if __name__ == '__main__':
    # NB DO NOT RUN THIS IF YOU DON'T UNDERSTAND IT.

    archyve: Archyve = Archyve(r"<put your path here>")

    # Get a list of all the duplicate images and videos
    archyve = archyve.images + archyve.videos
    duplicate_lists: list[list[Entry]] = archyve.images.duplicates()

    # Sort the duplicates by age
    for i in range(len(duplicate_lists)):
        duplicate_lists[i] = sorted(duplicate_lists[i], key=lambda e: e.created)

    # Delete the ones that are not the oldest
    delete: list[list[Entry]] = [duplicate_list[1:] for duplicate_list in duplicate_lists]
    for entry_list in delete:
        archyve.delete(entry_list)

