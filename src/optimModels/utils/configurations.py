from optimModels.utils.constantes import solverMethod



class kineticConfigurations:
    STEADY_STATE_TIME = 1e9
    SOLVER_METHOD = solverMethod.LSODA  # ode solver method used in the phenotype simulation
    SOLVER_TIMEOUT = 60  # maximum time allowed by simulation


class EAConfigurations:
    # Configuration of EA algorithm
    MAX_GENERATIONS = 10
    POPULATION_SIZE = 6
    MAX_CANDIDATE_SIZE = 6
    POPULATION_SELECTED_SIZE = 4
    NUM_ELITES = 1
    CROSSOVER_RATE = 0.9
    MUTATION_RATE = 0.1
    NEW_CANDIDATES_RATE = 0.1
    TOURNAMENT_SIZE = 3
    NUM_CPUS = 2
    NUM_BEST_SOLUTIONS = 2

    @staticmethod
    def get_default_config():
        return [EAConfigurations.POPULATION_SIZE, EAConfigurations.MAX_CANDIDATE_SIZE, EAConfigurations.CROSSOVER_RATE,
                EAConfigurations.MUTATION_RATE, EAConfigurations.NEW_CANDIDATES_RATE, EAConfigurations.NUM_ELITES]


