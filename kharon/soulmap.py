import hashlib


def make_soul_map(device):
    soul_map = {}

    for func in device.__dict__.values():
        m = hashlib.md5()
        m.update(func.__name__)
        soul_map['%s.%s' % (device.__name__, func.__name__)] = m.hexdigest()
    return soul_map
