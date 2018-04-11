from abc import ABCMeta, abstractmethod
from collections import OrderedDict

class OverrideSimulationProblem:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_modifications(self):
        pass

    @abstractmethod
    def simplify_modifications(self, simulationProblem, objFunction, fitness):
        pass

class OverrideStoicSimulProblem(OverrideSimulationProblem):
    """
            This class contains the modifications that will be made to the stoichiometric model in the simulation process.

            Attributes
            ----------
            constraints  : dict {recation_id : (LowerBound, UpperBound)}
                (KO simulation: LowerBound= UpperBound = 0)

        """

    def __init__(self, constraints={}):
        self.constraints = constraints

    def get_modifications(self):
        return self.constraints

    def get_bounds(self, reactionId):
        bounds = None
        if reactionId in self.constraints.keys():
            bounds = self.constraints.get(reactionId)
        return bounds

    def simplify_modifications(self, simulationProblem, objFunction, fitness):
        constraintsOrig = self.constraints.copy()

        for k in constraintsOrig.keys():
            del self.constraints[k]
            try:
                res = simulationProblem.simulate(self)
                #print(objFunction.get_name())
                newFitness = objFunction.get_fitness(res)
            except Exception:
                newFitness = -1.0
                #print(fitness)
                #print(newFitness)
            if round(fitness, 12) != round(newFitness, 12):
                #print("remove :" +k)
                self.constraints[k] = constraintsOrig[k]


class OverrideKineticSimulProblem(OverrideSimulationProblem):
    """
        This class contains the modifications that will be made to the kinetic model in the simulation process.

        Attributes
        ----------
        factors  : dict {id_param : factor_value}
            Factors to be multiplied with vmax parameter present in the model.
            (KO simulation: factor = 0, under expression: factor > 0 and <1, over expression factor >1)

    """
    def __init__(self, factors = {}):
        self.factors = factors

    def get_modifications(self):
        return self.factors

    def set_factors(self, values):
        if not isinstance(values, OrderedDict):
            raise Exception ("Factors must be of type OrderedDict, where the key is the parameter id (vmax) and the value a double!")
        self.factors = values


