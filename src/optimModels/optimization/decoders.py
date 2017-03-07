from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from optimModels.simulation.simulationProblems import kineticSimulationProblem,stoichiometricSimulationProblem
from optimModels.simulation.overrideSimulationProblem import overrideKineticSimProblem, overrideStoichSimProblem

class absDecoder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_override_simul_problem(self, candidate, simulProblem):
        pass

    @abstractmethod
    def candidate_decoded(self, candidate, model):
        pass




class decoderReactionsKnockouts(absDecoder):
    def __init__(self, reactionsIds):
        self.name_class = "decoderReactionsKnockouts"
        self.reactionsIds = reactionsIds

    def get_override_simul_problem(self, candidate, simulProblem):

        koReacs = self.candidate_decoded(candidate)

        if isinstance(simulProblem, stoichiometricSimulationProblem):
            modifications = OrderedDict([(r_id,(0.0,0.0)) for r_id in koReacs])
            override = overrideStoichSimProblem(modifications=modifications)
        elif isinstance(simulProblem, kineticSimulationProblem):
            factors = OrderedDict([(r_id, 0) for r_id in koReacs])
            override = overrideKineticSimProblem(factors=factors)
        else:
            raise Exception ("Unknown  simulation problem type by decoderReactionsKnockouts")
        return override

    # convert the index reaction for reaction ids
    def candidate_decoded(self, candidate):
        result = [self.reactionsIds[x] for x in list(candidate)]
        return result

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

class decoderUnderOverExpression(absDecoder):
    def __init__ (self, reactionsIds,  levels):
        self.reactionsIds = reactionsIds
        self.levels = levels
        self.name_class = "decoderUnderOverExpression"

    def get_override_simul_problem(self, candidate, simulProblem):
        if isinstance(simulProblem, stoichiometricSimulationProblem):
            pass  # TO DO

        elif isinstance(simulProblem, kineticSimulationProblem):
            solDecoded = self.candidate_decoded(candidate)
            override = overrideKineticSimProblem(factors=solDecoded)
            return override
        else:
            raise Exception ("Unknown  simulation problem type by decoderUnderOverExpression")

    def candidate_decoded(self, candidate):
        result = OrderedDict([(self.reactionsIds[k], self.levels[v]) for (k, v) in list(candidate)])
        return result

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)