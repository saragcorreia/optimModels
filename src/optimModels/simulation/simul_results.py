from optimModels.utils.constantes import solverStatus

class SimulationResult():
    """ Represents the result of a metabolic model simulation on steady-state.

        Attributes
        ------------
        modelId : str
            identification of metabolic model
        solverStatus: int
            simulation result (OPTIMAL = 0, UNKNOWN = 1, ERROR = 2).
        ssFluxesDistrib : dict
            fluxes distribution achieved in steady state.
        overrideSimulProblem: overrideKineticSimulProblem
            Modifications over the metabolic model.
        """

    def __init__(self, modelId, solverStatus, ssFluxesDistrib,
                 overrideSimulProblem=None):
        self.modelId = modelId
        self.solverStatus = solverStatus
        self.ssFluxesDistrib = ssFluxesDistrib
        self.overrideSimulProblem = overrideSimulProblem

    def get_solver_status(self):
        """
        Gets the solver status result.

        Returns
        ---------
        out : int
            Possible values: OPTIMAL = 1; UNKNOWN = 0; ERROR = 2;...
        """

        return self.solverStatus

    def get_override_simul_problem(self):
        """
        Gets the override simulation problem.

        Returns
        ---------
        out : overrideKineticSimulProblem
        """
        return self.overrideSimulProblem

    def get_fluxes_distribution(self):
        """
        Gets the steady-state flux distribution.

        Returns
        ---------
        out : dict
            Flux distribution in steady-state {reactionId: fluxValue}.
        """
        return self.ssFluxesDistrib

class StoicSimulationResult(SimulationResult):

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def print(self):
        print("Phenotype Simulation")
        print("------------------------")
        print("model id: " + self.modelId)
        print("status: " + solverStatus.get_status_str(self.solverStatus))
        print("fluxes: ")
        for k, v in self.ssFluxesDistrib.items():
            print("     " + k + " = " + str(v))

        if self.overrideSimulProblem:
            print("mofifications:")
            for k, v in self.overrideSimulProblem.get_modifications().items():
                print("     " + k + " = " + str(v))
        print("------------------------")

class kineticSimulationResult(SimulationResult):
    """ Represents the result of a dynamic metabolic model simulation on steady-state.

    Attributes
    ------------
    modelId : str
        identification of metabolic model
    solverStatus: int
        simulation result (OPTIMAL = 0, UNKNOWN = 1, ERROR = 2).
    ssFluxesDistrib : dict
        fluxes distribution achieved in steady state.
    ssConcentrations : dict
        metabolites concentration in steady state.
    overrideSimulProblem: overrideKineticSimulProblem
        Modifications over the metabolic model.
    """

    def __init__(self, modelId, solverStatus, ssFluxesDistrib, ssConcentrations=None,
                 overrideSimulProblem=None):
        self.ssConcentrations = ssConcentrations
        super().__init__(modelId, solverStatus,ssFluxesDistrib, overrideSimulProblem)


    def get_steady_state_concentrations(self):
        """
        Gets the metabolite concentrations in steady-state {metaboliteId: concentration value}.

        Returns
        ---------
        out : dict
        """
        return self.ssConcentrations



    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


    def print(self):
        print("Phenotype Simulation")
        print("------------------------")
        print("model id: " + self.modelId)
        print("status: " + solverStatus.get_status_str(self.solverStatus))
        print("fluxes: ")
        for k,v in self.ssFluxesDistrib.items():
            print("     " + k + " = " + str(v))

        print("concentrations: ")
        for k, v in self.ssConcentrations.items():
            print("     " + k + " = " + str(v))

        if self.overrideSimulProblem:
            print("mofifications:")
            for k,v in self.overrideSimulProblem.get_modifications().items():
                print("     " + k + " = " + str(v))
        print("------------------------")
