from collections import OrderedDict
from optimModels.model.dynamicModel import load_kinetic_model

def merge_two_dicts(x, y):
    """
        Merge two dictinaries, if the key are present in both, value of y[key] are maintained
        :param x: dictionary
        :param y: dictionary
        """
    if x is None:
        x = OrderedDict()
    if y is None:
        y = OrderedDict()
    z = x.copy()
    z.update(y)
    return z

def printModel ():
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    #sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
    model = load_kinetic_model(sbmlFile)

    for r in model.reactions:
        print r +" ----> "+  model.ratelaws[r]

    model.build_ode()
    print model._func_str



if __name__ == '__main__':
    printModel()
