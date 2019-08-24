import os

from filelock import FileLock

from savoten.repository.json_reader_writer import (json_read, json_write, lock,
                                                   unlock)

_dname = os.path.dirname
TEST_READ_FILE_NAME = os.path.join(_dname(os.path.abspath(__file__)), 'data',
                                   'json_read')
TEST_WRITE_FILE_NAME = os.path.join(_dname(os.path.abspath(__file__)), 'data',
                                    'json_write')
TEST_LOCK_FILE_NAME = os.path.join(_dname(os.path.abspath(__file__)), 'data',
                                   'lock_test')


def teardown_function():
    if os.path.exists(TEST_LOCK_FILE_NAME + '.lock'):
        os.remove(TEST_LOCK_FILE_NAME)
    if os.path.exists(TEST_WRITE_FILE_NAME):
        os.remove(TEST_WRITE_FILE_NAME)


def test_lock():
    test_file_name = TEST_LOCK_FILE_NAME
    actual = lock(test_file_name)
    assert isinstance(actual, FileLock)


def test_unlock():
    lock = FileLock(TEST_LOCK_FILE_NAME)
    unlock(lock)
    assert lock.is_locked is False


def test_json_read():
    test_file_name = TEST_READ_FILE_NAME
    expect_data = {"hoge": "fuga"}
    actual_data = json_read(filename=test_file_name)
    assert expect_data == actual_data


def test_json_write():
    test_file_name = TEST_WRITE_FILE_NAME
    expect_data = {"hoge": "fuga"}
    json_write(filename=test_file_name, data=expect_data)
    actual_data = json_read(filename=test_file_name)
    assert expect_data == actual_data
