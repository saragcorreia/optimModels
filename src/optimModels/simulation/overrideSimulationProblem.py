from collections import OrderedDict

class overrideStoichSimProblem():
    """
        This class contains the modifications that will be made to the stoichiometric model in the simulation process.

        Attributes
        ----------
        modifications : OrderedDict
            Environmental conditions to be applied in the metabolic model.

    """

    def __init__(self,modifications):
        self._modifications = modifications

    @property
    def modifications(self):
        return self._modifications

    @modifications.setter
    def modifications(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Modifications must be of type OrderedDict, where the key is the reaction id and the value a tuple of doubles!")
        self._modifications = values


class overrideKineticSimProblem():
    """
        This class contains the modifications that will be made to the kinetic model in the simulation process.

        Attributes
        ----------
        parameters : OrderedDict
            New parameters values to be applied to the model.
        factors: OrderedDict
            Factors to be multiplied with vmax / enzyme concentrations present in the model.
            (KO simulation: factor =0, under expression: factor > 0 and <1, over expression factor >1)

    """
    def __init__(self, parameters= None, factors = None):

        self._parameters = parameters
        self._factors = factors

    @property
    def parameters(self):
        """
            OrderedDict: Dictionary with the changed parameters to be apply in the model.

        """
        return self._parameters

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Parameters must be of type OrderedDict, where the key is the parameter id and the value a double!")
        self._parameters = values

    @property
    def factors(self):
        """
            OrderedDict: Dictionary with the modifications to be apply in the model.

        """
        return self._factors

    @factors.setter
    def factors(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Factors must be of type OrderedDict, where the key is the parameter id (vmax) and the value a double!")
        self._factors = values