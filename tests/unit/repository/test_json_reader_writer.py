from savoten.repository.json_reader_writer import json_read, json_write, lock, unlock

import os
import pathlib
import json
from filelock import FileLock
from unittest.mock import patch

_dname = os.path.dirname


def test_lock():
    test_file_name = _dname(os.path.abspath(__file__)) + '/data/lock_test'
    actual = lock(test_file_name)
    assert isinstance(actual, FileLock) 

def test_unlock():
    lock = FileLock('')
    unlock(lock)
    assert lock.is_locked is False

def test_json_read():
    test_file_name = _dname(os.path.abspath(__file__)) + '/data/json_read'
    expect_data = {"hoge": "fuga"}
    actual_data = json_read(filename=test_file_name)
    assert expect_data == actual_data


def test_json_write():
    test_file_name = _dname(os.path.abspath(__file__)) + '/data/json_write'
    pathlib.Path(test_file_name).touch()
    expect_data = json.dumps({"hoge": "fuga"})
    json_write(filename=test_file_name, data=expect_data)
    actual_data = json_read(filename=test_file_name)
    assert expect_data == actual_data
    os.remove(test_file_name)
