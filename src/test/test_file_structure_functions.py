from src.file_structure_functions import sub_files, sub_dirs, sub_paths
from src.test.run_unit_tests import TEST_MATERIALS
from pathlib import Path
from typing import Final
import unittest

TEST_MATS: Final[Path] = TEST_MATERIALS / 'file_structure_functions'


class TestFileStructureFunctions(unittest.TestCase):

    def test_sub_files(self):
        sf: list[Path] = list(sub_files(TEST_MATS / 'sub_files'))
        self.assertEqual(sf, [(TEST_MATS / 'sub_files' / f'file{i}.txt') for i in range(1, 5)])

    def test_sub_dir(self):
        sd: list[Path] = list(sub_dirs(TEST_MATS / 'sub_dirs'))
        self.assertEqual(sd, [(TEST_MATS / 'sub_dirs' / f'dir{i}') for i in range(1, 5)])

    def test_sub_paths(self):
        sp: list[Path] = list(sub_paths(TEST_MATS / 'sub_paths'))

        # Make sure we found all the files
        file_names = {path.stem for path in sp}
        for i in range(1, 21):
            self.assertIn(f'file{i}', file_names)

        # Make sure we didnt find any extra files
        assert len(file_names) == 20

        # Make sure all the paths we found actually exist
        for p in sp:
            assert p.exists()


if __name__ == '__main__':
    unittest.main()
