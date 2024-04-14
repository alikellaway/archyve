"""
Module contains a unit test for the entry module.

Author: ali.kellaway139@gmail.com
"""
from src.test.run_unit_tests import TEST_MATERIALS
from src.entry import EntryType, Entry
from unittest import TestCase, main
from datetime import datetime
from pathlib import Path
from typing import Final


ENTRY_TEST_MATS: Final[Path] = TEST_MATERIALS / 'entry'


class TestMediaTypes(TestCase):
    def test_entry_type(self):
        """
        Test that the get media type of function correctly identifies the media type of certain files based off their
        extensions.
        """
        # Test it can recognise some images
        self.assertEqual(Entry(ENTRY_TEST_MATS / 'image.jpg').entry_type, EntryType.IMAGE)
        self.assertEqual(Entry(ENTRY_TEST_MATS / 'image.png').entry_type, EntryType.IMAGE)
        # Test is can recognise some audio
        self.assertEqual(Entry(ENTRY_TEST_MATS / 'audio.wav').entry_type, EntryType.AUDIO)
        self.assertEqual(Entry(ENTRY_TEST_MATS / 'audio.mp3').entry_type, EntryType.AUDIO)
        # Test it can recognise some video
        self.assertEqual(Entry(ENTRY_TEST_MATS / 'video.mp4').entry_type, EntryType.VIDEO)
        self.assertEqual(Entry(ENTRY_TEST_MATS / 'video.mpeg').entry_type, EntryType.VIDEO)
        # Test it correctly outputs unknown when not recognized.
        self.assertEqual(Entry(ENTRY_TEST_MATS / 'unknown').entry_type, EntryType.UNKNOWN)
        self.assertEqual(Entry(ENTRY_TEST_MATS / 'unknown.1234').entry_type, EntryType.UNKNOWN)

    def test_equality(self):
        """
        Test that our equality override is functioning as intended.
        """
        self.assertTrue(Entry(ENTRY_TEST_MATS / 'black_square.jpg') == Entry(ENTRY_TEST_MATS / 'black_square.jpg'))
        self.assertTrue(Entry(ENTRY_TEST_MATS / 'black_square.jpg') == Entry(ENTRY_TEST_MATS / 'black_square1.jpg'))
        self.assertFalse(Entry(ENTRY_TEST_MATS / 'black_square.jpg') == Entry(ENTRY_TEST_MATS / 'image.jpg'))

    def test_lt(self):
        """
        Test that our less than override is working as intended.
        """
        self.assertTrue(Entry(ENTRY_TEST_MATS / 'image.jpg') < Entry(ENTRY_TEST_MATS / 'black_square.jpg'))
        self.assertFalse(Entry(ENTRY_TEST_MATS / 'image.jpg') < Entry(ENTRY_TEST_MATS / 'image.jpg'))
        self.assertFalse(Entry(ENTRY_TEST_MATS / 'black_square.jpg') < Entry(ENTRY_TEST_MATS / 'image.jpg'))

    # TODO come up with a better way to test created (as it will not work when cloned).
    # def test_created(self):
    #     """
    #     Test the created property is working as intended.
    #     :return:
    #     """
    #     self.assertEqual(Entry(ENTRY_TEST_MATS / 'black_square.jpg').created,
    #                      datetime.strptime('2024-04-08 20:34:01.332365', '%Y-%m-%d %H:%M:%S.%f'))
    #     self.assertEqual(Entry(ENTRY_TEST_MATS / 'video.mpeg').created,
    #                      datetime.strptime('2024-04-07 19:14:09.961920', "%Y-%m-%d %H:%M:%S.%f"))

    def test_exif(self):
        """
        Test that we can correctly acquire exif data about from an image entry.
        """
        self.assertTrue(Entry(ENTRY_TEST_MATS / 'image.jpg').exif is None)
        self.assertTrue(Entry(ENTRY_TEST_MATS / 'image_with_exif.jpg').exif is not None)


if __name__ == '__main__':
    main()
