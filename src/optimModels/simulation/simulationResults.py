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
    def __init__(self, modelId, fluxesDistribution=None, methodId=None, envCondictions=None):
        """ Represents the result of a stoichiometric metabolic model simulation
        @arguments:
        modelId: identification of metabolic model
        fluxesDistribution:
        methodId: method used in the simulation (FBA, MOMA, ROOM, etc)
        envCondictions: reactions constrains used in the simulation,  OrderedDict(ReacionId: (LowerBound, UpperBound)) (KO reactions will be represented with r_id:(0.0,0.0)
        """
        self.fluxesDistribution = fluxesDistribution
        self.methodId = methodId
        self.envCondictions = envCondictions

    def get_fluxes_distribution(self):
        return self.fluxesDistribution



class kineticSimulationResult(simulationResult):
    def __init__(self, modelId, fluxesDistribution=None, kineticParameters=None, factors=None, timePoint=None):
        """ Represents the result of a dynamic metabolic model simulation
        @arguments:
        modelId: identification of metabolic model
        fluxesDistribution: fluxes distribution
        kineticParameters: kinetic parameters changed
        factors: set of tuples (reactionId, value) that represents if the reaction was KO (value = 0), under (value <0) or over (value >0) expressed
        timePoint: time point used to steady state simulation.
        """
        self.fluxesDistribution = fluxesDistribution
        self.kineticParameters = kineticParameters
        self.factors = factors
        self.timePoint = timePoint

    def get_fluxes_distribution(self):
        return self.fluxesDistribution

    def get_factores(self):
        return self.factors

    def get_kinetic_parameters(self):
        return self.kineticParameters

    def get_time_point(self):
        return self.timePoint
