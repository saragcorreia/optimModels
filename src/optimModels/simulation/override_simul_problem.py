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
    """

    def __init__(self, constraints={}):
        """
        Create a instance of override stroichiometric simulation problem.
        Args:
            constraints (dict): Dictionary with the new constraints to be applied in the simulation ("reac_id": (LB, UB)).
        """
        self.constraints = constraints

    def get_modifications(self):
        return self.constraints


    def simplify_modifications(self, simulationProblem, objFunction, fitness):
        """
        Simplify the constraints to be applied in the simulation. Constraints that not influence the fitness value will
        be removed.

        Args:
            simulationProblem: simulation problem instance
            objFunction: function to calculate the fitness
            fitness: reference fitness

        """
        constraintsOrig = self.constraints.copy()
        for k in constraintsOrig.keys():
            del self.constraints[k]
            try:
                res = simulationProblem.simulate(self)
                newFitness = objFunction.get_fitness(res)
            except Exception:
                newFitness = -1.0
            if round(fitness, 12) != round(newFitness, 12):
                self.constraints[k] = constraintsOrig[k]


class OverrideKineticSimulProblem(OverrideSimulationProblem):
    """
    This class contains the modifications that will be made to the kinetic model in the simulation process.

    Args:
        factors  (dict): Factors to be multiplied with vmax parameter present in the model.
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


