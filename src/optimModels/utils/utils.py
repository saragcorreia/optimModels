from collections import OrderedDict

import  multiprocessing.pool

def fix_exchange_reactions_model(model):
    '''
    Convert the exchange reactions for the uptake reactions have negative fluxes and excretion reactions have positive fluxes.
    Args:
        model: Metabolic model

    Returns: a new copy of model where all exchange reactions are in the format " A <---> "

    '''
    newModel = model.copy();
    exchange = model.get_exchange_reactions(include_sink=True)
    for rId in exchange:
        reac = model.reactions[rId]
        if len(reac.get_products())>0:
            new_lb = -1 * reac.ub if reac.ub is not None else None
            new_ub = -1 * reac.lb if reac.lb is not None else None
            newModel.reactions[rId].lb = new_lb if new_lb !=0 else 0
            newModel.reactions[rId].ub = new_ub if new_ub !=0 else 0

            for m_id, coeff in reac.stoichiometry.items():
                newModel.reactions[rId].stoichiometry[m_id] = -1*coeff
    return newModel

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