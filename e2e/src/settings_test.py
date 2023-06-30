from os.path import isdir

from settings import TEST_DATA_DIR


def test_testdata_dir():
    assert isdir(TEST_DATA_DIR), TEST_DATA_DIR
