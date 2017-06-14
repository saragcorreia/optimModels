from abc import ABCMeta, abstractmethod

class objectiveFunction:
    """
    This abstract class should be extended by all implemented objective functions classes.

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_fitness(self, simulationResult):
        return


    @abstractmethod
    def method_str(self):
        return

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


class targetFlux(objectiveFunction):
    """
    This class implements the "target flux" objective function. The fitness is given by the flux value of the target reaction.

    Attributes
    ----------
    targetReactionId : str
        Reaction identifier of the target compound production.

    """
    def __init__(self, targetReactionId):
        self.targetReactionId = targetReactionId

    def get_fitness(self, simulResult):
        fluxes = simulResult.get_fluxes_distribution()
        if self.targetReactionId not in fluxes.keys():
            raise ValueError("Reaction id is not present i the fluxes distribution. Please check id objective function is correct.")
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




class BPCY (objectiveFunction):
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

    def get_fitness(self, simulResult):
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


def build_objective_function(id, args):
    """
    Parameters
    -----------
    id : str
        name of the objective function. The implemented objective functions should be registed in constants.objFunctions class
    args : list of str
        the number of arguments depends of the objective function chosen by user.

    """

    if id == BPCY.get_id():
        objFunc = BPCY(args[0],args[1],args[2])
    elif id == targetFlux.get_id():
        objFunc = targetFlux(args[0])
    else:
        raise Exception("Wrong objective function!")

    return objFunc