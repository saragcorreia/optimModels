from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.overrideSimulationProblem import overrideKineticSimulProblem

class decoder:
    """ Abstract class to define the required methods that must be implemented by all decoders.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_override_simul_problem(self, candidate, simulProblem):
        pass

    @abstractmethod
    def candidate_decoded(self, candidate, model):
        pass


class decoderKnockouts(decoder):
    """ Class to decode to convert a candidate solution in a list of identifiers used to simulate the KO reactions.

    Attributes
    -----------
    ids : list of str

    """
    def __init__(self, ids):

        self.ids = ids

    def get_override_simul_problem(self, candidate, simulProblem):
        """ Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the reactions knockouts.

        Parameters
        -----------
        candidate : list of int
            index of parameters .
        simulProblem : simulationProblem object
            contains all information required to perform a simulation of the model.

        Returns
        --------
        out : overrideKineticSimulProblem
            object with the modifications to be applied over the simulation Problem.

        """
        ko = self.candidate_decoded(candidate)

        if isinstance(simulProblem, kineticSimulationProblem):
            factors = OrderedDict([(r_id, 0) for r_id in ko])
            override = overrideKineticSimulProblem(factors=factors)
        else:
            raise Exception ("Unknown simulation problem type by decoderKnockouts.")
        return override

    def candidate_decoded(self, candidate):
        """ Convert the list of index into a list of ientifiers.

        Parameters
        -----------
            candidate : list of int
                indexes of parameters .

        Returns
        --------
            out : list of str
                parameters identifiers.
        """
        result = [self.ids[x] for x in list(candidate)]
        return result

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

class decoderUnderOverExpression(decoder):
    """ Class to convert a candidate solution repre identifiers used to simulate the under/ over enzyme expression.

    Attributes
    -----------
    ids : list of str
        parameters identifiers to be used in the optimization
    levels : list of float
        levels of expression

    """
    def __init__ (self, ids,  levels):
        self.ids = ids
        self.levels = levels

    def get_override_simul_problem(self, candidate, simulProblem):
        """ Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the under/over enzymes expression.

        Parameters
        -----------
        candidate : map of type *{parameterIndex : levelIndex}*
            candidate represented using indexes.
        simulProblem : simulationProblem object
            contains all information required to perform a simulation of the model.

        Returns
        ---------
        out : overrideKineticSimulProblem
            object with the modifications to be applied over the simulation Problem.
        """
        if isinstance(simulProblem, kineticSimulationProblem):
            solDecoded = self.candidate_decoded(candidate)
            override = overrideKineticSimulProblem(factors=solDecoded)
            return override
        else:
            raise Exception ("Unknown simulation problem type by decoderUnderOverExpression")

    def candidate_decoded(self, candidate):
        """ Convert the map of type *{parameterIndex : levelIndex}* to a map of type *{parameterId: levelOfExpression}*

        Parameters
        -----------
        candidate : map
            The key is the parameter index and the value is the level of expression index.

        Returns
        --------
        out : map
            The key is the parameter id and the value is the level of expression with values between 0 and 1 to represent under expression or higher that 1 to represent the over expression.
        """
        result = {self.ids[k]: self.levels[v] for (k, v) in list(candidate)}
        return result

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)