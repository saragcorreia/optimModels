from abc import ABCMeta, abstractmethod

class simulationResult:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_fluxes_distribution(self):
        pass

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)



# NOT USED ... YET
class stoichiometricSimulationResult(simulationResult):
    def __init__(self, modelId, steadysatefluxesDistrib=None, methodId=None, modifications=None):
        """ Represents the result of a stoichiometric metabolic model simulation
        @arguments:
        modelId: identification of metabolic model
        steadysatefluxesDistrib: fluxes distribution achieved in steady state
        methodId: method used in the simulation (FBA, MOMA, ROOM, etc)
        modifications: constraints used in the simulation,  OrderedDict(ReacionId: (LowerBound, UpperBound)) (KO reactions will be represented with r_id:(0.0,0.0)
        """
        self.steadysatefluxesDistrib = steadysatefluxesDistrib
        self.methodId = methodId
        self.modifications = modifications

    def get_fluxes_distribution(self):
        return self.steadysatefluxesDistrib


class kineticSimulationResult(simulationResult):
    def __init__(self, modelId, steadysatefluxesDistrib=None, modifications=None, factors=None, timePoint=None):
        """ Represents the result of a dynamic metabolic model simulation
        @arguments:
        modelId: identification of metabolic model
        steadysatefluxesDistrib: fluxes distribution achieved in steady state
        modifications (dictionary): kinetic parameters changed {paramId: value}
        factors: set of tuples (reactionId, value) that represents if the reaction was KO (value = 0), under (value <0) or over (value >0) expressed
        timePoint: time point used in steady state simulation.
        """
        self.steadysatefluxesDistrib = steadysatefluxesDistrib
        self.modifications = modifications
        self.factors = factors
        self.timePoint = timePoint

    def get_fluxes_distribution(self):
        return self.steadysatefluxesDistrib

    def get_factores(self):
        return self.factors

    def get_modificationss(self):
        return self.modifications

    def get_time_point(self):
        return self.timePoint
