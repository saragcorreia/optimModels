import time
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from optimModels.utils.utils import merge_two_dicts, MyPool
from optimModels.simulation.simulationResults import kineticSimulationResult, stoichiometricSimulationResult
from optimModels.simulation.solvers import odespySolver
from  optimModels.utils.constantes import solverStatus, solverId, solverMethod

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
        return


# NOT USED .. YET
class stoichiometricSimulationProblem(simulationProblem):
    """
        This class contains all required information to perform a simulation of a kinetic metabolic model.

        Attributes
        ------------------
        model : dynamicModel
            Metabolic model object.
        modifications : dict
            Modifications or/and environmental conditions to be aplied to the model (optional).
        objFlux : str
            Reaction to maximize/minimize
        solverId : int
            Identification of solver (CPLEX, GLPK, etc)
        solverMethod : int
            Identification of method (FBA, ROOM, MOMA, etc)

    """

    def __init__(self, model, modifications, objFlux, solverId, solverMethod,):
        self.model = model
        self.modifications = modifications
        self.objFlux = objFlux
        self.solverId = solverId
        self.solverMethod = solverMethod

    # TO DO
    def simulate(self, overrideProblem=None):
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
        ------------------
        model : dynamicModel
            Metabolic model object.
        parameters : dict
            New parameters values to be aplied to the model (optional).
        factors : dict (optional)
            Factors to be multiplied with vmax / enzyme concentrations present in the model.
            (KO simulation: factor = 0, under expression: factor > 0 and < 1, over expression factor >1.
        t_steps : list
            list of exact time steps to evaluate (default: [0,1e9])
        timeout : int
            Maximum time in secounds allowed to perform the simulation.
        solverId: int
            Solver identifier (default: odespy package)
        solverMethod : int
            Method used by solver (default LSODA)

    """

    def __init__(self, model, parameters=None, factors=OrderedDict(), tSteps=[0, 1e9],
                 timeout=None, solverId=solverId.ODESPY, solverMethod=solverMethod.LSODA, ):
        self.model = model
        self.parameters = parameters
        self.factors = factors
        self.tSteps = tSteps
        self.timeout = timeout
        self.solverId = solverId
        self.solverMethod = solverMethod

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

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
        solverId : int
            Identification of solver method present on the class *odeSolver*.
        overrideProblem : overrideKineticSimProblem
            Modification over the kinetic model

        Returns
        --------
        out : kineticSimulationResult
            Returns an object of type kineticSimulationResult with the steady-state flux distribution.
        """

        if overrideSimulProblem is None:
            final_params = self.parameters
            final_factors = self.factors
        else:
            final_params = merge_two_dicts(self.parameters, overrideSimulProblem.parameters)
            final_factors = merge_two_dicts(self.factors, overrideSimulProblem.factors)

        # required to have fluxes rates in the end of solver.solve, otherwise the reference given on get_ode function is lost!!!
        final_rates = OrderedDict()

        # update initial concentrations when a [enz] is changed: ==0, up or down regulated
        initConcentrations = self.get_initial_concentrations().copy()

        common = set(self.model.metabolites).intersection(final_factors.keys())
        if len(common) > 0:
            for enz in common:
                newVal = initConcentrations[enz] * final_factors[enz]
                initConcentrations[enz] = newVal

        # print "Initial concentrations"
        # print initConcentrations

        # print self.timeout
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
        return kineticSimulationResult(self.get_model().id, solverStatus=status, steadysatefluxesDistrib=sstateRates,
                                       solverMethod=solverId, overrideSimulProblem=overrideSimulProblem)


# Auxiliar functions
# required to avoid the pickling the solver.solve function
def _my_kinetic_solve(model, final_rates, final_params, final_factors, solverId, initialConc, timePoints):
    f = model.get_ode(r_dict=final_rates, params=final_params, factors=final_factors)
    func = lambda x, t: f(t, x)

    solver = odespySolver(solverId).get_solver(func)
    solver.set_initial_condition(initialConc)
    # print "INIT solve"
    X, t = solver.solve(timePoints)
    # print "concentrations"
    # print model.metabolites.keys()
    # print X
    return final_rates
