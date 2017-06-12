from collections import OrderedDict

import  multiprocessing.pool

class MyTree:
    "Generic tree node."
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
       # assert isinstance(node, MyTree)
        self.children.append(node)

def get_order_nodes(tree):
    if tree.children is None:
        return [tree.name];
    else:
        res = []
        for child in tree.children:
            res = res + get_order_nodes(child)
        return res


def merge_two_dicts(x, y):
    if x is None:
        x = OrderedDict()
    if y is None:
        y = OrderedDict()
    z = x.copy()
    z.update(y)
    return z


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess