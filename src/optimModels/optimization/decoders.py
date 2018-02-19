from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from optimModels.simulation.simul_problems import KineticSimulationProblem, StoicSimulationProblem
from optimModels.simulation.override_simul_problem import OverrideKineticSimulProblem, OverrideStoicSimulProblem
from optimModels.utils.configurations import StoicConfigurations

class Decoder:
    """ Abstract class to define the required methods that must be implemented by all decoders.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_override_simul_problem(self, candidate, simulProblem):
        pass

    @abstractmethod
    def decode_candidate(self, candidate):
        pass

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)



class _DecoderIds(Decoder):

    def __init__(self, ids):
        self.ids = ids

    def decode_candidate(self, candidate):
        """ Convert the list of index into a list of identifiers.

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


    def decode_candidate_ids_to_index(self, identifiers):
        """ Convert the list of identifiers into a list of integers (indexes).

        Parameters
        -----------
            identifiers : list of str
                ids of parameters .

        Returns
        --------
            out : list of int
                indexes of parameters.
        """
        result =  [self.ids.index(x) for x in identifiers]
        return result

    @abstractmethod
    def get_override_simul_problem(self, candidate, simulProblem):
        pass

class _DecoderIdsAndLevels(Decoder):
    def __init__(self, ids, levels):
        self.ids = ids
        self.levels = levels


    def decode_candidate(self, candidate):
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

    def decode_candidate_ids_to_index(self, identifiers):
        """ Convert the list of tupples of identifiers into a list of tuples of integers (indexes).

        Parameters
        -----------
            identifiers : list of tuples
                ids of parameters .

        Returns
        --------
            out : list of tuples
                indexes of parameters.
        """
        result = [(self.ids.index(x), self.levels.index(y)) for x, y in identifiers.items()]
        return result

    @abstractmethod
    def get_override_simul_problem(self, candidate, simulProblem):
        pass

class DecoderMediumLevels(_DecoderIdsAndLevels):
    def get_override_simul_problem(self, candidate, simulProblem):

        uptake = self.decode_candidate(candidate)
        drains = [r  for r in simulProblem.get_drains() if r not in simulProblem.get_constraints_reacs() and r not in simulProblem.objective.keys()]

        if isinstance(simulProblem, StoicSimulationProblem):
            # close all drains to uptake and open only the reaction in candidate
            constraints = {}
            for rId in drains:
                if rId in uptake.keys():
                    constraints[rId] = (-1* uptake[rId],0)
                else:
                    constraints[rId] = (0, StoicConfigurations.DEFAULT_UB)
            override = OverrideStoicSimulProblem(constraints=constraints)
        else:
            raise Exception ("Unknown simulation problem type by DecoderMedium.")

        return override


class DecoderMediumReacKO(Decoder):

    def __init__(self, idsDrains, idsReactions):
        self.drains = idsDrains
        self.reactions = idsReactions
        for r in idsReactions:
            print (r)

    def decode_candidate(self, candidate):
        """ Convert the list of index into a list of identifiers.

        Parameters
        -----------
            candidate : list of int
                indexes of parameters .

        Returns
        --------
            out : list of str
                parameters identifiers.
        """
        drains = [self.drains[x] for x in list(candidate[0])]
        ko = [self.reactions[x] for x in list(candidate[1])]
        return drains, ko


    def decode_candidate_ids_to_index(self, identifiers):
        """ Convert the list of identifiers into a list of integers (indexes).

        Parameters
        -----------
            identifiers : list of str
                ids of parameters .

        Returns
        --------
            out : list of int
                indexes of parameters.
        """
        indexDrains =  [self.drains.index(x) for x in identifiers[0]]
        indexKO =[self.reactions.index(x) for x in identifiers[1]]
        return indexDrains, indexKO

    def get_override_simul_problem(self, candidate, simulProblem):

        """ Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the drains that will be open for uptake.

        Parameters
        -----------
        candidate : list of int
            index of reactions that will be open (drains) or the flux will be 0 (internal reactions).
        simulProblem : simulationProblem object
            contains all information required to perform a simulation of the model.

        Returns
        --------
        out : overrideSimulProblem
            object with the modifications to be applied over the simulation Problem.

        """

        uptake, koReactions = self.decode_candidate(candidate)

        if isinstance(simulProblem, StoicSimulationProblem):
            # close all drains to uptake and open only the reaction in candidate
            constraints = {reacId:(0, 0) for reacId in koReactions}
            for rId in self.drains:
                if rId in uptake:
                    constraints[rId] = (StoicConfigurations.DEFAULT_LB,0)
                else:
                    constraints[rId] = (0, StoicConfigurations.DEFAULT_UB)
            override = OverrideStoicSimulProblem(constraints=constraints)
        else:
            raise Exception ("Unknown simulation problem type by DecoderMediumReacKO.")

        return override



class DecoderMedium(_DecoderIds):

    def get_override_simul_problem(self, candidate, simulProblem):

        """ Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the drains that will be open for uptake.

        Parameters
        -----------
        candidate : list of int
            index of reactions that will be open.
        simulProblem : simulationProblem object
            contains all information required to perform a simulation of the model.

        Returns
        --------
        out : overrideSimulProblem
            object with the modifications to be applied over the simulation Problem.

        """

        uptake = self.decode_candidate(candidate)
        #drains = [r  for r in simulProblem.get_drains() if r not in simulProblem.get_constraints_reacs()]

        if isinstance(simulProblem, StoicSimulationProblem):
            # close all drains to uptake and open only the reaction in candidate
            constraints = {}
            for rId in self.ids:
                if rId in uptake:
                    constraints[rId] = (StoicConfigurations.DEFAULT_LB,0)
                else:
                    constraints[rId] = (0, StoicConfigurations.DEFAULT_UB)
            override = OverrideStoicSimulProblem(constraints=constraints)
        else:
            raise Exception ("Unknown simulation problem type by DecoderMedium.")

        return override



class DecoderReacKnockouts(_DecoderIds):
    """ Class to decode to convert a candidate solution in a list of identifiers used to simulate the KO reactions.

    Attributes
    -----------
    ids : list of reactions ids

    """

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
        out : OverrideKineticSimulProblem
            object with the modifications to be applied over the simulation Problem.

        """
        ko = self.decode_candidate(candidate)

        if isinstance(simulProblem, KineticSimulationProblem):
            factors = OrderedDict([(r_id, 0) for r_id in ko])
            override = OverrideKineticSimulProblem(factors=factors)
        elif isinstance(simulProblem, StoicSimulationProblem):
            constraints = {reacId:(0, 0) for reacId in ko}
            override = OverrideStoicSimulProblem(constraints=constraints)
        else:
            raise Exception ("Unknown simulation problem type by DecoderReacKnockouts.")

        return override



class DecoderReacUnderOverExpression(_DecoderIdsAndLevels):
    """ Class to convert a candidate solution repre identifiers used to simulate the under/ over enzyme expression.

    Attributes
    -----------
    ids : list of str
        parameters identifiers to be used in the optimization
    levels : list of float
        levels of expression

    """


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
        out : OverrideKineticSimulProblem
            object with the modifications to be applied over the simulation Problem.
        """
        if isinstance(simulProblem, KineticSimulationProblem):
            solDecoded = self.decode_candidate(candidate)
            override = OverrideKineticSimulProblem(factors=solDecoded)
            return override
        else:
            raise Exception ("Unknown simulation problem type by decoderUnderOverExpression")