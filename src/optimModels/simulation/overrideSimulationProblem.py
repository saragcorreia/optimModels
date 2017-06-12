from collections import OrderedDict

class overrideKineticSimulProblem():
    """
        This class contains the modifications that will be made to the kinetic model in the simulation process.

        Attributes
        ----------
        factors  : dict
            Factors to be multiplied with vmax present in the model.
            (KO simulation: factor = 0, under expression: factor > 0 and <1, over expression factor >1)

    """
    def __init__(self, factors = None):
        self.factors = factors

    def get_factors(self):
        return self.factors

    def set_factors(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Factors must be of type OrderedDict, where the key is the parameter id (vmax) and the value a double!")
        self.factors = values