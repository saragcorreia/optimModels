from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from optimModels.simulation.simul_problems import KineticSimulationProblem, StoicSimulationProblem, GeckoSimulationProblem
from optimModels.simulation.override_simul_problem import OverrideKineticSimulProblem, OverrideStoicSimulProblem
from optimModels.utils.configurations import StoicConfigurations


class Decoder:
    """
    Abstract class with the abstract methods that must be implemented by all decoders.
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


class DecoderMediumLevels(Decoder):
    def __init__(self, ids, levels):
        self.ids = ids
        self.levels = levels

    def decode_candidate(self, candidate):
        """
        Convert the map of type *{parameterIndex : levelIndex}* to a map of type *{parameterId: levelOfExpression}*

        Args:
            candidate (dict): The key is the parameter index and the value is the level of expression index.

        Returns: A dictionary where the key is the parameter id and the value is the level of expression with values between
            0 and 1 to represent under expression or higher that 1 to represent the over expression.
        """
        result = {self.ids[k]: self.levels[v] for (k, v) in list(candidate)}
        return result

    def decode_candidate_ids_to_index(self, identifiers):
        """ Convert the list of tupples of identifiers into a list of tuples of integers (indexes).

        Args:
            identifiers (list): List of tuples whit the parameters and levels ids

        Returns: List of tuples indexes of parameters.
        """
        result = [(self.ids.index(x), self.levels.index(y)) for x, y in identifiers.items()]
        return result

    def get_override_simul_problem(self, candidate, simulProblem):
        """
        Function to create a instance of OverrideSimulationProblem based on the candidate given by argument.
        Args:
            candidate (list): candidate to decode
            simulProblem: Simulation problem instance.

        Returns: OverrideStoicSimulProblem instance

        """
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

    def decode_candidate(self, candidate):
        """
        Convert the list of index into a list of identifiers.
        Args:
            candidate(list): list of indexes of parameters

        Returns: list of parameters ids.
        """
        drains = [self.drains[x] for x in list(candidate[0])]
        ko = [self.reactions[x] for x in list(candidate[1])]
        return drains, ko

    def decode_candidate_ids_to_index(self, identifiers):
        """
        Convert the list of identifiers into a list of integers (indexes).
        Args:
            identifiers (list): parameters identifiers

        Returns: List of parameters indexes.
        """
        indexDrains =  [self.drains.index(x) for x in identifiers[0]]
        indexKO =[self.reactions.index(x) for x in identifiers[1]]
        return indexDrains, indexKO

    def get_override_simul_problem(self, candidate, simulProblem):
        """
        Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the drains that will be open for uptake and KO reactions.
        Args:
            candidate (list):  indexes of reactions that will be open (drains) or the flux will be 0 (internal reactions).
            simulProblem (SimulationProblem): all information required to perform a model simulation.

        Returns: OverrideSimulProblem instance with the modifications to be applied over the simulation Problem.
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

class DecoderMedium(Decoder):
    def __init__(self, ids):
        self.ids = ids

    def decode_candidate(self, candidate):
        """ Convert the list of indexes into a list of identifiers.

        Args:
            candidate (list): indexes of parameters.

        Returns: list of parameters identifiers.

        """
        result = [self.ids[x] for x in list(candidate)]
        return result

    def decode_candidate_ids_to_index(self, identifiers):
        """
        Convert the list of identifiers into a list of integers (indexes).

        Args:
            identifiers (list): Ids of parameters

        Returns: List of integers (parameters indexes)

        """
        result = [self.ids.index(x) for x in identifiers]
        return result

    def get_override_simul_problem(self, candidate, simulProblem):

        """ Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the drains that will be open for uptake.
        Args:
            candidate (list):  indexes of reactions that will be open (drains).
            simulProblem (SimulationProblem): all information required to perform a model simulation.

        Returns: OverrideSimulProblem instance with the modifications to be applied over the simulation Problem.
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

class DecoderReacKnockouts(Decoder):
    def __init__(self, ids):
        self.ids = ids

    def decode_candidate(self, candidate):
        """ Convert the list of indexes into a list of identifiers.

        Args:
            candidate (list): indexes of parameters/reactions.

        Returns: list of parameters/reactions identifiers.

        """
        result = [self.ids[x] for x in list(candidate)]
        return result

    def decode_candidate_ids_to_index(self, identifiers):
        """
        Convert the list of identifiers into a list of integers (indexes).

        Args:
            identifiers (list): Ids of parameters/reactions

        Returns: List of integers (parameters indexes)

        """
        result = [self.ids.index(x) for x in identifiers]
        return result

    def get_override_simul_problem(self, candidate, simulProblem):
        """ Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the reactions knockouts.

        Args:
            candidate (list):  indexes of reactions.
            simulProblem (SimulationProblem): all information required to perform a model simulation.

        Returns: OverrideSimulProblem instance with the modifications to be applied over the simulation Problem.
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


class DecoderReacUnderOverExpression(Decoder):
    def __init__(self, ids, levels):
        self.ids = ids
        self.levels = levels

    def decode_candidate(self, candidate):
        """
        Convert the map of type *{parameterIndex : levelIndex}* to a map of type *{parameterId: levelOfExpression}*

        Args:
            candidate (dict): The key is the parameter index and the value is the level of expression index.

        Returns: A dictionary where the key is the parameter id and the value is the level of expression with values between
            0 and 1 to represent under expression or higher that 1 to represent the over expression.
        """
        result = {self.ids[k]: self.levels[v] for (k, v) in list(candidate)}
        return result

    def decode_candidate_ids_to_index(self, identifiers):
        """ Convert the list of tuples of identifiers into a list of tuples of integers (indexes).

        Args:
            identifiers (list): List of tuples whit the parameters and levels ids

        Returns: List of tuples indexes of reactions.
        """
        result = [(self.ids.index(x), self.levels.index(y)) for x, y in identifiers.items()]
        return result

    def get_override_simul_problem(self, candidate, simulProblem):
        """ Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the under/over enzymes expression.
        Args:
            candidate (dict):  candidate represented using reactions and levels indexes.
            simulProblem (SimulationProblem): all information required to perform a model simulation.

        Returns: OverrideSimulProblem instance with the modifications to be applied over the simulation Problem.
        """
        if isinstance(simulProblem, KineticSimulationProblem):
            solDecoded = self.decode_candidate(candidate)
            override = OverrideKineticSimulProblem(factors=solDecoded)
            return override
        else:
            raise Exception ("Unknown simulation problem type by decoderUnderOverExpression")

class DecoderProtKnockouts(Decoder):
    def __init__(self, ids):
        self.ids = ids

    def decode_candidate(self, candidate):
        """ Convert the list of indexes into a list of identifiers.

        Args:
            candidate (list): indexes of parameters.

        Returns: list of parameters identifiers.

        """
        result = [self.ids[x] for x in list(candidate)]
        return result

    def decode_candidate_ids_to_index(self, identifiers):
        """
        Convert the list of identifiers into a list of integers (indexes).

        Args:
            identifiers (list): Ids of proteins

        Returns: List of integers (proteins indexes)

        """
        result = [self.ids.index(x) for x in identifiers]
        return result

    def get_override_simul_problem(self, candidate, simulProblem):
        """ Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the protein knockouts.

        Args:
            candidate (list):  indexes of proteins.
            simulProblem (SimulationProblem): all information required to perform a model simulation.

        Returns: OverrideSimulProblem instance with the modifications to be applied over the simulation Problem.
        """
        ko = ["draw_prot_"+ p for p in self.decode_candidate(candidate)]

        if  isinstance(simulProblem, GeckoSimulationProblem):
            constraints = {reacId:(0, 0) for reacId in ko}
            override = OverrideStoicSimulProblem(constraints=constraints)
        else:
            raise Exception ("Unknown simulation problem type by DecoderProtKnockouts.")

        return override

class DecoderProtUnderOverExpression(Decoder):
    def __init__(self, ids, levels):
        self.ids = ids
        self.levels = levels

    def decode_candidate(self, candidate):
        """
        Convert the map of type *{proteinIndex : levelIndex}* to a map of type *{proteinId: levelOfExpression}*

        Args:
            candidate (dict): The key is the parameter index and the value is the level of expression index.

        Returns: A dictionary where the key is the protein id and the value is the level of expression with values between
            0 and 1 to represent under expression or higher that 1 to represent the over expression.
        """
        result = {self.ids[k]: (0,self.levels[v]) for (k, v) in list(candidate)}
        return result

    def decode_candidate_ids_to_index(self, identifiers):
        """ Convert the list of tupples of identifiers into a list of tuples of integers (indexes).

        Args:
            identifiers (list): List of tuples whit the proteins and levels ids

        Returns: List of tuples indexes.
        """
        result = [(self.ids.index(x), self.levels.index(y)) for x, y in identifiers.items()]
        return result

    def get_override_simul_problem(self, candidate, simulProblem):
        """ Build the override simulation problem which will contains the modifications that must be applied to the model in order to simulate the under/over proteins expression.
        Args:
            candidate (dict):  candidate represented using proteins and levels indexes.
            simulProblem (SimulationProblem): all information required to perform a model simulation.

        Returns: OverrideSimulProblem instance with the modifications to be applied over the simulation Problem.
        """
        if isinstance(simulProblem, KineticSimulationProblem):
            solDecoded = self.decode_candidate(candidate)

            constraints = {"draw_prot"+k: v for k,v  in solDecoded}
            override = OverrideStoicSimulProblem(constraints=constraints)
        else:
            raise Exception ("Unknown simulation problem type by decoderUnderOverExpression")
        return override