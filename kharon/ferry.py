import hashlib


def make_map(device):

    comm_map = {}
    for func in device.__dict__.values():
        m = hashlib.md5()
        m.update(func.__name__)
        comm_map['%s.%s' % (device.__name__, func.__name__)] = m.hexdigest()
    return comm_map
