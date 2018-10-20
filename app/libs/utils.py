import hashlib


def get_md5(pwd):
    h = hashlib.md5()
    h.update(pwd)
    return h.hexdigest()