import time
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from optimModels.utils.utils import merge_two_dicts, MyPool
from optimModels.simulation.simulationResults import kineticSimulationResult
from optimModels.simulation.solvers import odespySolver
from optimModels.utils.configurations import kineticConfigurations
from optimModels.utils.constantes import solverStatus

try:
    import cPickle as pickle
except ImportError:
    import pickle


class simulationProblem:
    __metaclass__ = ABCMeta

    @abstractmethod
    def simulate(self, solverId, overrideProblem):
        return

class kineticSimulationProblem(simulationProblem):
    """
        This class contains all required information to perform a simulation of a kinetic metabolic model.

        Attributes
        ------------------
        model : dynamicModel
            Metabolic model object.
        factors : dict (optional)
            Factors to be multiplied with vMax parameters present in the model.
            (KO simulation: factor = 0, under expression: factor > 0 and < 1, over expression factor >1.
        t_steps : list
            list of exact time steps to evaluate (default: [0,1e9])
        timeout : int
            Maximum time in secounds allowed to perform the simulation.

    """

    def __init__(self, model, factors=OrderedDict(), tSteps=[0, 1e9], timeout=None):
        self.model = model
        self.factors = factors
        self.tSteps = tSteps
        self.timeout = timeout

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def get_model(self):
        return self.model

    def get_initial_concentrations(self):
        return self.model.concentrations

    def get_time_steps(self):
        return self.tSteps

    def get_number_reactions(self):
        return len(self.model.reactions)

    def get_model(self):
        return self.model

    def simulate(self, overrideSimulProblem=None):
        """
        This method preform the phenotype simulation of the kinetic model, using the solverId method and applying the modifications present in the instance of overrideSimulProblem.

        Parameters
        -----------
        overrideProblem : overrideKineticSimProblem
            Modification over the kinetic model.

        Returns
        --------
        out : kineticSimulationResult
            Returns an object of type kineticSimulationResult with the steady-state flux distribution and concentrations.
        """

        if overrideSimulProblem is None:
            final_factors = self.factors
        else:
            final_factors = merge_two_dicts(self.factors, overrideSimulProblem.factors)

        # required to have fluxes rates in the end of solver.solve, otherwise the reference given on get_ode function is lost!!!
        final_rates = OrderedDict()

        # update initial concentrations when a [enz] is changed: == 0, up or down regulated
        initConcentrations = self.get_initial_concentrations().copy()

        status = solverStatus.OPTIMAL
        t1 = time.time()
        if self.timeout is None:
            sstateRates, sstateConc, status = _my_kinetic_solve(self.get_model(), final_rates, final_factors,
                                            initConcentrations.values(),
                                            self.get_time_steps())
        else:
            p = MyPool(processes=1)
            res = p.apply_async(_my_kinetic_solve, (
                self.get_model(), final_rates, final_factors, initConcentrations.values(),
                self.get_time_steps()))
            try:
                sstateRates, sstateConc, status = res.get(self.timeout)  # Wait timeout seconds for func to complete.
            except Exception:
                print("Aborting due to timeout")
                sstateRates = {}
                status = solverStatus.ERROR
                p.terminate()
            p.close()
            p.join()
        t2 = time.time()
        print "TIME (seconds) simulate: " + str(t2 - t1)

        return kineticSimulationResult(self.get_model().id, solverStatus=status, ssFluxesDistrib=sstateRates,
                                       ssConcentrations = sstateConc,
                                       overrideSimulProblem=overrideSimulProblem)


# Auxiliar functions
# required to avoid the pickling the solver.solve function
def _my_kinetic_solve(model, final_rates, final_factors, initialConc, timePoints):
    f = model.get_ode(r_dict=final_rates, factors=final_factors)
    func = lambda x, t: f(t, x)

    solver = odespySolver(kineticConfigurations.SOLVER_METHOD).get_solver(func)
    solver.set_initial_condition(initialConc)

    try:
        X, t = solver.solve(timePoints)
    except Exception:
        print "Error on solver!!!"
        return {},[], solverStatus.ERROR

    return final_rates, X[1],solverStatus.OPTIMAL
