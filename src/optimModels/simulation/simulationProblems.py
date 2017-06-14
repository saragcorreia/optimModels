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
        model : kineticModel
            Metabolic model object.
        parameters : dict (optional)
            New values for the parameters present in the model.
        t_steps : list
            list of exact time steps to evaluate (default: [0,1e9])
        timeout : int
            Maximum time in secounds allowed to perform the simulation.

    """

    def __init__(self, model, parameters=None, tSteps=[0, 1e9], timeout=None):
        self.model = model
        self.parameters = parameters
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

        final_factors = {}
        if overrideSimulProblem:
            final_factors = overrideSimulProblem.factors
        # update initial concentrations when a [enz] is changed: == 0, up or down regulated
        initConcentrations = self.get_initial_concentrations().copy()

        t1 = time.time()
        if self.timeout is None:
            sstateRates, sstateConc, status = _my_kinetic_solve(self.get_model(), self.parameters,
                                                                final_factors,
                                                                initConcentrations.values(),
                                                                self.get_time_steps())
        else:
            p = MyPool(processes=1)
            res = p.apply_async(_my_kinetic_solve, (
                self.get_model(), self.parameters, final_factors, initConcentrations.values(),
                self.get_time_steps()))
            try:
                sstateRates, sstateConc, status = res.get(self.timeout)  # Wait timeout seconds for func to complete.
            except Exception:
                print("Aborting due to timeout")
                sstateRates = {}
                sstateConc = {}
                status = solverStatus.ERROR
                p.terminate()
            p.close()
            p.join()
        t2 = time.time()
        print "TIME (seconds) simulate: " + str(t2 - t1)

        return kineticSimulationResult(self.get_model().id, solverStatus=status, ssFluxesDistrib=sstateRates,
                                       ssConcentrations=sstateConc,
                                       overrideSimulProblem=overrideSimulProblem)



def _my_kinetic_solve(model, finalParameters, finalFactors, initialConc, timePoints):
    """
    Private function: auxiliary function required to avoid the pickling the solver.solve function

    """
    finalRates = OrderedDict()
    f = model.get_ode(r_dict=finalRates, params=finalParameters, factors=finalFactors)
    func = lambda x, t: f(t, x)

    solver = odespySolver(kineticConfigurations.SOLVER_METHOD).get_solver(func)
    solver.set_initial_condition(initialConc)

    try:
        X, t = solver.solve(timePoints)
    except Exception:
        print "Error on solver!!!"
        #print X
        #print finalRates
        return {}, {}, solverStatus.ERROR

    conc = OrderedDict(zip(model.metabolites.keys(), X[1]))
    return finalRates, conc, solverStatus.OPTIMAL
