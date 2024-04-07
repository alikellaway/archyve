"""
Module contains a unit test for the media_types module.

Author: ali.kellaway139@gmail.com
"""
from src.toolkit.media_types import get_media_type_of, MediaType
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
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'image.jpg'), MediaType.IMAGE)
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'image.png'), MediaType.IMAGE)
        # Test is can recognise some audio
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'audio.wav'), MediaType.AUDIO)
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'audio.mp3'), MediaType.AUDIO)
        # Test it can recognise some video
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'video.mp4'), MediaType.VIDEO)
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'video.mpeg'), MediaType.VIDEO)
        # Test it correctly outputs unknown when not recognized.
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'unknown'), MediaType.UNKNOWN)
        self.assertEqual(get_media_type_of(MEDIA_TYPES_TEST_MATERIALS / 'unknown.1234'), MediaType.UNKNOWN)
