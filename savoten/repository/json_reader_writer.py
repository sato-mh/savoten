import json

import filelock


def lock(filename):

    return filelock.FileLock(filename + ".lock", timeout=1)


def unlock(lock):

    if isinstance(lock, filelock.FileLock):
        lock.release()
    else:
        raise TypeError


def json_write(filename, data):

    with open(filename, "w") as f:
        json.dump(data, f)


def json_read(filename):

    with open(filename, "r") as f:
        return json.load(f)
