from .archyve import Archyve
from typing import Final
from pathlib import Path
from .entry import Entry
import test


TEST_DIR: Final[Path] = Path(test.__file__).parent


def entries_to_str(entry_matrix: list[list[Entry]]) -> list[list[str]]:
    """
    Converts matrix of paths to a matrix of strings just so I can print out and show the results.
    :param entry_matrix: The matrix of paths to convert to strings
    :return: A matrix of strings.
    """
    return [[str(entry.path) for entry in entry_list] for entry_list in entry_matrix]


def identify_duplicate_files(directory: Path | str) -> list[list[Entry]]:
    """
    Finds duplicate files in the given directory.
    :param directory: The parent directory to search for duplicates in
    :return: A list of lists containing files that have the same contents.
    """
    archive: Archyve = Archyve(directory)
    return archive.duplicates()


def identify_duplicate_images(directory: Path | str) -> list[list[Entry]]:
    """
    Showing how you can find duplicate images in an archive.
    :param directory: The directory in which to find duplicate images.
    :return: A list of lists of paths to files that have the same contents.
    """
    archive: Archyve = Archyve(directory)  # Create an archive in the area you want
    return archive.images.duplicates()  # Get duplicate images from the archive


def identify_entries_with_custom_filter(directory: Path | str) -> list[Entry]:
    archyve: Archyve = Archyve(directory)
    archyve: Archyve = archyve.filter(lambda e: 'black' in e.path.name.casefold())
    return list(archyve.entries)


if __name__ == '__main__':
    def breaker():
        print('-' * 100)

    breaker()
    print("The following are duplicate files from the unit test folder:".upper())
    print("\n".join(
        str(entry_list) for entry_list in entries_to_str(identify_duplicate_files(TEST_DIR)))
    )

    breaker()
    print("The following are duplicate images from the unit test folder:".upper())
    print("\n".join(
        str(entry_list) for entry_list in entries_to_str(identify_duplicate_images(TEST_DIR)))
    )

    breaker()
    print("The following are all the files in the test folder with 'black' in the file name:".upper())
    print("\n".join(str(p) for p in identify_entries_with_custom_filter(TEST_DIR)))

