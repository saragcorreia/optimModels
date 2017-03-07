from abc import ABCMeta, abstractmethod

class objectiveFunction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_fitness(self, simulationResult):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def method_str(self):
        pass

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

class targetFlux(objectiveFunction):
    def __init__(self, targetReactionId):
        self.targetReactionId = targetReactionId

    def get_fitness(self, simulResult):
        fluxes = simulResult.get_fluxes_distribution()
        if self.targetReactionId not in fluxes.keys():
            raise ValueError("Reaction id is not present i the fluxes distribution. Please check id objective function is correct.")
        return fluxes[self.targetReactionId]

    def get_name(self):
        return "Target Flux"

    def method_str(self):
        return "Target Flux: " + self.targetReactionId

class BPCY (objectiveFunction):
    def __init__(self, biomassId, productId, uptakeId):
        self.biomassId = biomassId
        self.productId = productId
        self.uptakeId = uptakeId

    def get_fitenss(self, simulResult):
        ssFluxes= simulResult.get_fluxes_distribution()
        if self.biomassId not in ssFluxes.keys or self.productId not in ssFluxes.keys:
            raise ValueError("Reaction ids is not present in the fluxes distribution. Please check id objective function is correct.")
        return (ssFluxes[self.biomass] * ssFluxes[self.productId])/ssFluxes[self.uptakeId]

    def get_name(self):
        return "Biomass-Product Coupled Yield"

    def method_str(self):
        return "BPCY =  (" + self.biomassId + " * " + self.productId +") / " + self.uptakeId