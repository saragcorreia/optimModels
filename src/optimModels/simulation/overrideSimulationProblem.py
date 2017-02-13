from collections import OrderedDict

class overrideStoichSimProblem():
    def __init__(self,envConditions):
        self._envConditions = envConditions

    @property
    def enConditions(self):
        return self._envConditions

    @enConditions.setter
    def enConditions(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Factors must be of type OrderedDict, where the key is the reaction id and the value a tuple of doubles!")
        self._envConditions = values


class overrideKineticSimProblem():
    def __init__(self, parameters= None, factors = None):
  #      self._rates = rates
        self._parameters = parameters
        self._factors = factors

 #   @property
 #   def rates(self):
 #       return self._rates

 #   @rates.setter
 #   def rates(self, values):
 #       if not isinstance(values, OrderedDict):
 #           raise Exception ("Factors must be of type OrderedDict, where the key is the reaction id and the value a double!")
 #       self._rates = values

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Factors must be of type OrderedDict, where the key is the reaction id and the value a double!")
        self._parameters = values

    @property
    def factors(self):
        return self._factors

    @factors.setter
    def factors(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Factors must be of type OrderedDict, where the key is the reaction id and the value a double!")
        self._factors = values