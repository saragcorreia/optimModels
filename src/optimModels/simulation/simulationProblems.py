import time
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from numpy import linspace
from optimModels.utils.utils import merge_two_dicts
from optimModels.utils.utils import MyPool

from optimModels.simulation.simulationResults import kineticSimulationResult, stoichiometricSimulationResult
from optimModels.simulation.solvers import odeSolver
from  optimModels.utils.constantes import solverStatus

try:
    import cPickle as pickle
except ImportError:
    import pickle


class simulationProblem:
    __metaclass__ = ABCMeta

    def get_model(self):
        return self._model

    @abstractmethod
    def simulate(self, solverId, overrideProblem):
        pass

# NOT USED .. YET
class stoichiometricSimulationProblem(simulationProblem):
    def __init__(self, model, modifications, objFunc, method):
        self._model = model
        self._modifications = modifications
        self._objFunc = objFunc
        self._method = method

    # TO DO
    def simulate(self, solverId, overrideProblem=None):
        # newEnvCond = merge(self.envConditions, overrideProblem.envConditions)
        print "stoichiometric model simulation!"
        print "TO DO"  # SGC: using framed / CAMEO / ???
        res = stoichiometricSimulationResult(self.get_model().id, [], "FBA", OrderedDict())

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


class kineticSimulationProblem(simulationProblem):
    """
        This class contains all required information to perform a simulation of a kinetic metabolic model.

        Attributes
        ----------
        model : dynamicModel
            Metabolic model object.

        parameters: dict (optional)
            New parameters values to be aplied to the model.
        factors: dict (optional)
            Modification
        time: float
            final simulation time (optional if t_steps is used instead)
        steps: int
            number of simulations steps (default: 100)
        t_steps: list
            list of exact time steps to evaluate (optional)
        timeout: int
            Maximum time in secounds allowed to perform the simulation.

    """
    def __init__(self, model, parameters=None, factors=OrderedDict(), time=1e9, steps=10000, tSteps=None,
                 timeout=None):
        self._model = model
        self._parameters = parameters
        self._factors = factors
        self._time = time
        self._steps = steps
        self._tSteps = tSteps
        self._timeout = timeout

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, params):
        self._parameters = params

    @property
    def factors(self):
        return self._factors

    @factors.setter
    def factors(self, factors):
        self._factors = factors

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    def get_initial_concentrations(self):
        return self._model.concentrations

    def get_time_steps(self):
        if self._tSteps is None:
            self._tSteps = linspace(0, self._time, self._steps)
        return self._tSteps

    def get_number_reactions(self):
        return len(self._model.reactions)

    def get_model(self):
        return self._model

    def simulate(self, solverId, overrideProblem=None):
        """
         bla bla bla

        :param solverId: int
        :param overrideProblem: overrideKineticSimProblem
        :return: kineticSimulationResult
        """

        if overrideProblem is None:
            final_params = self.parameters
            final_factors = self.factors
        else:
            final_params = merge_two_dicts(self.parameters, overrideProblem.parameters)
            final_factors = merge_two_dicts(self.factors, overrideProblem.factors)

        # required to have fluxes rates in the end of solver.solve, otherwise the reference given on get_ode function is lost!!!
        final_rates = OrderedDict()

        # update initial concentrations when a [enz] is changed: ==0, up or down regulated
        initConcentrations = self.get_initial_concentrations().copy()


        common = set(self._model.metabolites).intersection(final_factors.keys())
        if len (common)>0:
            for enz in common:
                newVal = initConcentrations[enz] * final_factors[enz]
                initConcentrations[enz] =newVal

        # print "Initial concentrations"
        # print initConcentrations

        #print self.timeout
        status = solverStatus.OPTIMAL
        t1 = time.time()
        if self.timeout is None:
            sstateRates = _my_kinetic_solve(self.get_model(), final_rates, final_params, final_factors, solverId,
                                            initConcentrations.values(),
                                            self.get_time_steps())
        else:
            p = MyPool(processes=1)
            res = p.apply_async(_my_kinetic_solve, (
                self.get_model(), final_rates, final_params, final_factors, solverId, initConcentrations.values(),
                self.get_time_steps()))
            try:
                sstateRates = res.get(self.timeout)  # Wait timeout seconds for func to complete.
            except Exception:
                print("Aborting due to timeout")
                sstateRates = {}
                status = solverStatus.ERROR
                p.terminate()
            p.close()
            p.join()
        t2 = time.time()
        print "TIME (seconds) simulate: " + str(t2 - t1)
        return kineticSimulationResult(self.get_model().id, solverStatus= status, steadysatefluxesDistrib = sstateRates, factors=final_factors,
                                       timePoint=self.get_time_steps()[-1])




# Auxiliar functions
# required to avoid the pickling the solver.solve function
def _my_kinetic_solve(model, final_rates, final_params, final_factors, solverId, initialConc, timePoints):
    f = model.get_ode(r_dict=final_rates, params=final_params, factors=final_factors)
    func = lambda x, t: f(t, x)

    solver = odeSolver(solverId).get_solver(func)
    solver.set_initial_condition(initialConc)
    #print "INIT solve"
    X, t = solver.solve(timePoints)
    #print "Concentracoes"
    # print model.metabolites.keys()
    #print X
    return final_rates




