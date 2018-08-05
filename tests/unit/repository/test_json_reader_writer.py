from savoten.repository.json_reader_writer import (
    json_read, json_write, lock, unlock
)
import os
from filelock import FileLock

_dname = os.path.dirname
_test_read_file_name = os.path.join(
        _dname(os.path.abspath(__file__)),
        'data',
        'json_read'
    )
_test_write_file_name = os.path.join(
        _dname(os.path.abspath(__file__)),
        'data',
        'json_write'
    )
_test_lock_file_name = os.path.join(
    _dname(os.path.abspath(__file__)),
    'data',
    'lock_test'
)


def teardown_function():
    if os.path.exists(_test_lock_file_name + '.lock'):
        os.remove(_test_lock_file_name)
    if os.path.exists(_test_write_file_name):
        os.remove(_test_write_file_name)


def test_lock():
    test_file_name = _test_lock_file_name
    actual = lock(test_file_name)
    assert isinstance(actual, FileLock)


def test_unlock():
    lock = FileLock('')
    unlock(lock)
    assert lock.is_locked is False


def test_json_read():
    test_file_name = _test_read_file_name
    expect_data = {"hoge": "fuga"}
    actual_data = json_read(filename=test_file_name)
    assert expect_data == actual_data


def test_json_write():
    test_file_name = _test_write_file_name
    expect_data = {"hoge": "fuga"}
    json_write(filename=test_file_name, data=expect_data)
    actual_data = json_read(filename=test_file_name)
    assert expect_data == actual_data
