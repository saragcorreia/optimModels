from abc import ABCMeta, abstractmethod

class absObjectiveFunction:
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

class targetFlux(absObjectiveFunction):
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

class BPCY (absObjectiveFunction):
    def __init__(self, biomassId, productId, uptakeId):
        self.biomassId = biomassId
        self.productId = productId
        self.uptakeId = uptakeId

    def get_fitenss(self, simulResult):
        fluxes= simulResult.get_fluxes_distribution()
        if self.biomassId not in fluxes.keys or self.productId not in fluxes.keys:
            raise ValueError("Reaction ids is not present in the fluxes distribution. Please check id objective function is correct.")
        return (fluxes[self.biomass] * fluxes[self.productId])/fluxes[self.uptakeId]

    def get_name(self):
        return "Biomass-Product Coupled Yield"

    def method_str(self):
        return "BPCY =  (" + self.biomassId + " * " + self.productId +") / " + self.uptakeId