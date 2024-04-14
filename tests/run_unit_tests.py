"""
Module contains logic to run all unit tests within the project.

Author: ali.kellaway139@gmail.com
"""
from unittest import TestSuite, defaultTestLoader, TextTestRunner
from pathlib import Path
from typing import Final


TEST_MATERIALS: Final[Path] = Path(__file__).parent / 'test_materials'


if __name__ == '__main__':
    test_suite: TestSuite = defaultTestLoader.discover(start_dir=str(Path(__file__).parent), pattern='test_*.py')
    TextTestRunner().run(test_suite)
