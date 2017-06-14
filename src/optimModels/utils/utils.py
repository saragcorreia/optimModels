from collections import OrderedDict

import  multiprocessing.pool

class MyTree:
    """Class to implement a generic tree."""

    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
        self.children.append(node)

def get_order_nodes(tree):
    """
    Returns the order of nodes

    Parameters
    -----------
        tree : instance of MyTree

    """
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
    """
    Extension of class *multiprocessing.Process* which make 'daemon' attribute always return False
    """

    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


class MyPool(multiprocessing.pool.Pool):
    """
    Note : sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
    because the latter is only a wrapper function, not a proper class.
    """
    Process = NoDaemonProcess