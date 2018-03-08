from abc import ABCMeta, abstractmethod

from optimModels.utils.configurations import StoicConfigurations
class EvaluationFunction:
    """
    This abstract class should be extended by all implemented evaluation functions classes.

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_fitness(self, simulationResult, candidate):
        return


    @abstractmethod
    def method_str(self):
        return

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

class MinNumberReacAndMaxFlux(EvaluationFunction):
    #TODO: Validar o que acontece em caso do ub do target ser 0 ou seja o fluxes[rId] é negativo (ver se há hipotese de isto acontecer)

    def __init__(self, maxCandidateSize, levels, maxTargetFlux):
        self.maxCandidateSize = maxCandidateSize
        self.levels = levels
        self.objective = maxTargetFlux

    def get_fitness(self, simulResult, candidate):
        fluxes = simulResult.get_fluxes_distribution()
        maxUptake = len(candidate) * self.levels[-1]
        sumUptake = 0
        sumObj = 0

        for rId in candidate.keys():
            sumUptake = sumUptake + candidate[rId]

        for rId, ub in self.objective.items():
            ub = StoicConfigurations.DEFAULT_UB if ub is None else ub
            f = 1 if fluxes[rId]>=ub else 1-((ub-fluxes[rId])/ub)
            sumObj = sumObj + f
        objFactor=sumObj/len(self.objective)

        # best solution when factores are close to 1
        upFactor = sumUptake/maxUptake
        lenFactor = len(candidate)/ self.maxCandidateSize

        return  objFactor/(upFactor * lenFactor)


    def method_str(self):
        return "Minimize the number and the fluxes of active reactions."

    @staticmethod
    def get_id():
        return "MinNumberReacAndMaxFlux"

    @staticmethod
    def get_name():
        return "Minimum number and fluxes of active reactions."

    @staticmethod
    def get_parameters_ids():
        return ["list of reactions ids", ""]

class MinNumberReac(EvaluationFunction):
    """
    This class implements ...

    Attributes
    ----------
    reactionList: list

    minFluxes : dict
        (key: reaction id, value: minimum of flux)

    """
    def __init__(self, maxCandidateSize, minFluxes):
        self.maxCandidateSize = maxCandidateSize
        self.minFluxes = minFluxes

    def get_fitness(self, simulResult, candidate):
        fluxes = simulResult.get_fluxes_distribution()
        for rId, flux in self.minFluxes.items():
            if fluxes[rId]< flux:
                return 0

        return 1 - len(candidate)/(self.maxCandidateSize + 1)

    def method_str(self):
        return "Minimum number of active reactions."

    @staticmethod
    def get_id():
        return "MinNumberReac"

    @staticmethod
    def get_name():
        return "Minimum number of active reactions."

    @staticmethod
    def get_parameters_ids():
        return ["list of reactions ids", ""]



class targetFlux(EvaluationFunction):
    """
    This class implements the "target flux" objective function. The fitness is given by the flux value of the target reaction.

    Attributes
    ----------
    targetReactionId : str
        Reaction identifier of the target compound production.

    """
    def __init__(self, targetReactionId):
        #TODO: take only the first element
        self.targetReactionId = targetReactionId[0]

    def get_fitness(self, simulResult, candidate):
        fluxes = simulResult.get_fluxes_distribution()
        if self.targetReactionId not in list(fluxes.keys()):
            raise ValueError("Reaction id is not present in the fluxes distribution.")
        return fluxes[self.targetReactionId]

    def method_str(self):
        return "Target Flux: " + self.targetReactionId

    @staticmethod
    def get_id():
        return "targetFlux"

    @staticmethod
    def get_name():
        return "Target Flux"

    @staticmethod
    def get_parameters_ids():
        return ["Target reaction id"]




class BPCY (EvaluationFunction):
    """
        This class implements the "Biomass-Product Coupled Yield" objective function. The fitness is given by the equation:
        (biomass_flux * product_flux)/ uptake_flux

        Attributes
        ----------
        biomassId : str
            biomass reaction identifier
        productId : str
            target product reaction identifier
        uptakeId : str
            reaction of uptake

        """
    def __init__(self, biomassId, productId, uptakeId):
        self.biomassId = biomassId
        self.productId = productId
        self.uptakeId = uptakeId

    def get_fitness(self, simulResult, candidate):
        ssFluxes= simulResult.get_fluxes_distribution()
        if self.biomassId not in ssFluxes.keys or self.productId not in ssFluxes.keys:
            raise ValueError("Reaction ids is not present in the fluxes distribution. Please check id objective function is correct.")
        return (ssFluxes[self.biomass] * ssFluxes[self.productId])/ssFluxes[self.uptakeId]



    def method_str(self):
        return "BPCY =  (" + self.biomassId +  " * " + self.productId +") / " + self.uptakeId

    @staticmethod
    def get_id():
        return "BPCY"

    @staticmethod
    def get_name():
        return "Biomass-Product Coupled Yield"

    @staticmethod
    def get_parameters_ids():
        return ["Biomass id", "Product id", "Uptake id"]


def build_evaluation_function(id, *args):
    """
    Parameters
    -----------
    id : str
        name of the objective function. The implemented objective functions should be registed in constants.objFunctions class
    *args : list of str
        the number of arguments depends of the objective function chosen by user.

    """

    if id == BPCY.get_id():
        objFunc = BPCY(args[0],args[1],args[2])
    elif id == targetFlux.get_id():
        objFunc = targetFlux(args[0])
    elif id == MinNumberReac.get_id():
        objFunc = MinNumberReac(args[0], args[1])
    elif id == MinNumberReacAndMaxFlux.get_id():
        objFunc = MinNumberReacAndMaxFlux (args[0], args[1],args[2])
    else:
        raise Exception("Wrong objective function!")

    return objFunc

