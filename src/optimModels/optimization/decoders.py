from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from optimModels.simulation.simulationProblems import kineticSimulationProblem,stoichiometricSimulationProblem


class absDecoder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_simulation_problem(self, candidate, simulProblem):
        pass

    @abstractmethod
    def candidate_decoded(self, candidate, model):
        pass

class decoderReactionsKnockouts(absDecoder):

    def update_simulation_problem(self, candidate, simulProblem):
        if isinstance(simulProblem, stoichiometricSimulationProblem):
            pass # TO DO change the envCondition to LB=UB=0 in the ko reactions

        elif isinstance(simulProblem, kineticSimulationProblem):
            koReacs = self.individual_decoded_str(candidate, simulProblem.model)
            # change ode func to set the new KO reaction set
            simulProblem.reset_parameters()
            simulProblem.set_reactions_ko(koReacs)
            simulProblem.update_obj()

        # convert the index reaction for reaction ids
    def candidate_decoded(self, candidate, model):
        reacsList = model.reactions.keys()
        result = [reacsList[x] for x in list(candidate)]
        return result


class decoderUnderOverExpression(absDecoder):
    def __init__ (self, levels):
        self.levels = levels

    def update_simulation_problem(self, candidate, simulProblem):
        if isinstance(simulProblem, stoichiometricSimulationProblem):
            pass  # TO DO

        elif isinstance(simulProblem, kineticSimulationProblem):
            solDecoded = self.individual_decoded_str(candidate, simulProblem.model)
            simulProblem.reset_parameters()
            simulProblem.set_factors(solDecoded)
            simulProblem.update_obj()

    def candidate_decoded(self, candidate, model):
        reacsList = model.reactions.keys()
        result = OrderedDict([(reacsList[k], self.levels[v]) for (k, v) in list(candidate)])
        return result
