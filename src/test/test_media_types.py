"""
Module contains a unit test for the media_types module.

Author: ali.kellaway139@gmail.com
"""
from src.toolkit.entry import get_media_type_of, EntryType
from src.test.run_unit_tests import TEST_MATERIALS
from unittest import TestCase
from pathlib import Path
from typing import Final


MEDIA_TYPES_TEST_MATERIALS: Final[Path] = TEST_MATERIALS / 'media_types'


class TestMediaTypes(TestCase):
    def test_get_media_type_of(self):
        """
        Test that the get media type of function correctly identifies the media type of certain files based off their
        extensions.
        """
        # Test it can recognise some images
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'image.jpg'), EntryType.IMAGE)
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'image.png'), EntryType.IMAGE)
        # Test is can recognise some audio
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'audio.wav'), EntryType.AUDIO)
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'audio.mp3'), EntryType.AUDIO)
        # Test it can recognise some video
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'video.mp4'), EntryType.VIDEO)
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'video.mpeg'), EntryType.VIDEO)
        # Test it correctly outputs unknown when not recognized.
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'unknown'), EntryType.UNKNOWN)
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'unknown.1234'), EntryType.UNKNOWN)
