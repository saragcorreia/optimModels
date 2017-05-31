from collections import OrderedDict

class overrideStoichSimulProblem():
    """
        This class contains the modifications that will be made to the stoichiometric model in the simulation process.

        Attributes
        ----------
        modifications : dict
            Environmental conditions to be applied in the metabolic model.
    """

    def __init__(self,modifications):
        self.modifications = modifications

    def get_modifications(self):
        return self.modifications


    def set_modifications(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Modifications must be of type OrderedDict, where the key is the reaction id and the value a tuple of doubles!")
        self.modifications = values


class overrideKineticSimulProblem():
    """
        This class contains the modifications that will be made to the kinetic model in the simulation process.

        Attributes
        ----------
        parameters : dict
            New parameters values to be applied to the model.
        factors  : dict
            Factors to be multiplied with vmax / enzyme concentrations present in the model.
            (KO simulation: factor =0, under expression: factor > 0 and <1, over expression factor >1)

    """
    def __init__(self, parameters= None, factors = None):
        self.parameters = parameters
        self.factors = factors

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Parameters must be of type OrderedDict, where the key is the parameter id and the value a double!")
        self.parameters = values

    def get_factors(self):
        return self._factors

    def set_factors(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Factors must be of type OrderedDict, where the key is the parameter id (vmax) and the value a double!")
        self.factors = values