from optimModels.utils.constantes import solverMethod


class SolverConfigurations:
    ABSOLUTE_TOL = 1e-9
    RELATIVE_TOL = 1e-6
    N_STEPS =10000

class StoicConfigurations:
    SOLVER = 'cplex'
    SOLVER_METHOD = 'pFBA'
    DEFAULT_LB = -99999
    DEFAULT_UB = 99999

class KineticConfigurations:
    STEADY_STATE_TIME = 1e9
    SOLVER = "odespy"
    SOLVER_METHOD = solverMethod.LSODA  # ode solver method used in the phenotype simulation
    SOLVER_TIMEOUT = 6000  # maximum time allowed by simulation




