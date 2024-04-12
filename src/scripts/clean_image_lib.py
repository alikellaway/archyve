"""
Script contains logic to analyse and clean an image library. The goal is to remove duplicates, keeping the oldest
copy that we can find. We also want to flatten the entire library, so that the user can sort by date manually and drag
into albums.

Author: ali.kellaway139@gmail.com
"""
from src.archive import Archive
from src.entry import Entry


if __name__ == '__main__':
    archive: Archive = Archive(r"D:\Pictures\Out Of Albums\Unsortables")

    # Get a list of all the duplicate images and videos
    duplicate_lists: list[list[Entry]] = archive.duplicates(archive.images, archive.videos)

    # Sort the duplicates by age
    for i in range(len(duplicate_lists)):
        duplicate_lists[i] = sorted(duplicate_lists[i], key=lambda e: e.created)

    print(duplicate_lists)
