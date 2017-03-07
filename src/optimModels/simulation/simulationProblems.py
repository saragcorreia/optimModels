import time
import copy
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from numpy import linspace
from optimModels.utils.utils import merge_two_dicts

from optimModels.simulation.simulationResults import kineticSimulationResult, stoichiometricSimulationResult
from optimModels.simulation.solvers import odeSolver
import multiprocessing
# We must import this explicitly, it is not imported by the top-level
# multiprocessing module.
import multiprocessing.pool
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
    def __init__(self, model, parameters=None, rates=None, factors=None, time=1e9, steps=10000, tSteps=None,
                 timeout=None):
        self._model = model
        self._parameters = parameters
        self._rates = rates
        self._factors = factors
        self._time = time
        self._steps = steps
        self._tSteps = tSteps
        self._timeout = timeout

        self._f = self._model.get_ode(r_dict=self.rates, params=self.parameters, factors=self.factors)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_f']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.update_func()

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, params):
        self._parameters = params
        self.update_func()

    @property
    def rates(self):
        return self._rates

    @rates.setter
    def rates(self, rates):
        self._rates = rates
        self.update_func()

    @property
    def factors(self):
        return self._factors

    @factors.setter
    def factors(self, factors):
        self._factors = factors
        self.update_func()

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    def get_initial_concentrations(self):
        return self._model.concentrations.values()

    def get_time_steps(self):
        if self._tSteps is None:
            self._tSteps = linspace(0, self._time, self._steps)
        return self._tSteps

    def get_number_reactions(self):
        return len(self._model.reactions)

    def get_model(self):
        return self._model

    def update_func(self):
        self._f = self._model.get_ode(r_dict=self.rates, params=self.parameters, factors=self.factors)

    def func(self, x, t):
        # f2 = lambda x, t: self.f(t, x)
        return self._f(t, x)

    def simulate(self, solverId, overrideProblem=None):
        if overrideProblem is None:
            final_rates = self.rates
            final_params = self.parameters
            final_factors = self.factors
        else:
            # final_rates = merge_two_dicts(self.rates, overrideProblem.rDict)
            final_rates = self.rates
            final_params = merge_two_dicts(self.parameters, overrideProblem.parameters)
            final_factors = merge_two_dicts(self.factors, overrideProblem.factors)

        # required to have fluxes rates in the end of solver.solve, otherwise the reference given on get_ode function is lost!!!
        if final_rates is None:
            final_rates = OrderedDict()

        # build the ODEs with the modification present in the override problem
        f = self.get_model().get_ode(r_dict=final_rates, params=final_params, factors=final_factors)

        #swap the arguments order
        func = lambda x, t: f(t, x)
        solver = odeSolver(solverId).get_solver(func)
        solver.set_initial_condition(self.get_initial_concentrations())

        #print self.timeout
        status = solverStatus.OPTIMAL
        t1 = time.time()
        if self.timeout is None:
            sstateRates = _my_kinetic_solve(self.get_model(), final_rates, final_params, final_factors, solverId,
                                            self.get_initial_concentrations(),
                                            self.get_time_steps())
        else:
            p = multiprocessing.pool.ThreadPool(processes=1)
            res = p.apply_async(_my_kinetic_solve, (
            self.get_model(), final_rates, final_params, final_factors, solverId, self.get_initial_concentrations(),
            self.get_time_steps()))
            try:
                sstateRates = res.get(self.timeout)  # Wait timeout seconds for func to complete.
            except Exception:
                print("Aborting due to timeout")
                p.terminate()
                sstateRates = {}
                status = solverStatus.ERROR
        t2 = time.time()
        print "TIME (seconds) simulate: " + str(t2 - t1)

        return kineticSimulationResult(self.get_model().id, solverStatus= status, steadysatefluxesDistrib = sstateRates, factors=final_factors,
                                       timePoint=self.get_time_steps()[- 1])


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
    #print model.metabolites.keys()
    #print X
    return final_rates




