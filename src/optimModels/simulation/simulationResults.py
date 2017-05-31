from abc import ABCMeta, abstractmethod
from optimModels.simulation.solvers import odespySolver


class simulationResult:
    """
    Abstract class to represent the results given by the simulation process.
    """
    __metaclass__ = ABCMeta

    def __init__(self, modelId, solverStatus, steadysatefluxesDistrib=None, solverId = None, solverMethod=None):
        self.modelId = modelId
        self.solverStatus = solverStatus
        self.steadysatefluxesDistrib = steadysatefluxesDistrib
        self.solverId = solverId
        self.solverMethod = solverMethod

    def get_fluxes_distribution(self):
        """
        Gets the steady-state flux distribution.

        Returns
        ---------
        out : dict
            Flux distribution in steady state {reactionId: fluxValue}.
        """
        return self.steadysatefluxesDistrib

    def get_solver_status(self):
        """
        Gets the solver status result.

        Returns
        ---------
        out : int
            Possible values: OPTIMAL = 0; UNKNOWN = 1; ERROR = 2
        """

        return self.solverStatus

    @abstractmethod
    def get_solver_id(self):
        return

    @abstractmethod
    def get_solver_method(self):
        return

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


# NOT USED ... YET
class stoichiometricSimulationResult(simulationResult):
    """ Represents the result of a stoichiometric metabolic model simulation

    Attributes
    ----------
    modelId : str
        identification of metabolic model
    steadysatefluxesDistrib : dict
        fluxes distribution achieved in steady state
    solverId: int
        solver identifier (CPLEX, GLPK, etc)
    solverMethod : int
        method used in the simulation (FBA, MOMA, ROOM, etc)
    modifications: dict
        constraints used in the simulation,  OrderedDict(ReacionId: (LowerBound, UpperBound)) (KO reactions will be represented with r_id:(0.0,0.0)
    """

    def __init__(self, modelId, solverStatus, steadysatefluxesDistrib=None, solverId = None, solverMethod=None, modifications=None):
        simulationResult.__init__(self, modelId, solverStatus, steadysatefluxesDistrib, solverId, solverMethod)
        self.modifications = modifications

    def get_solver_method(self):
        """
        Gets the solver method name.

        Returns
        ---------
        out : str
        """
        return "FBA" # TO CHANGE


class kineticSimulationResult(simulationResult):
    """ Represents the result of a dynamic metabolic model simulation.

    Attributes
    ------------
    modelId : str
        identification of metabolic model
    steadysatefluxesDistrib : dict
        fluxes distribution achieved in steady state
    solverId: int
        solver identifier (CPLEX, GLPK, etc)
    solverMethod : int
        Solver method used in the simulation (available methods present in odeSolver class).
    overrideSimulProblem: overrideKineticSimulProblem
        Modifications over the metabolic model.

    """

    def __init__(self, modelId, solverStatus, steadysatefluxesDistrib=None, solverId=None, solverMethod=None,
                 overrideSimulProblem=None):
        simulationResult.__init__(self, modelId, solverStatus, steadysatefluxesDistrib, solverId, solverMethod)
        self.overrideSimulProblem = overrideSimulProblem

    def get_solver_method(self):
        """
        Gets the solver identifyer.

        Returns
        ---------
        out : str
        """
        return "Odespy package"

    def get_solver_method(self):
        """
        Gets the solver method name.

        Returns
        ---------
        out : str
        """
        return odespySolver.get_solver_method_name(self.solverMethod)

    def get_override_simul_problem(self):
        """
        Gets the override simulation problem.

        Returns
        ---------
        out : overrideKineticSimulProblem
        """
        return self.overrideSimulProblem;
