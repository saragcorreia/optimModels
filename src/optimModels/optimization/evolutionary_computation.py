from random import Random
from multiprocessing import cpu_count
from inspyred import ec

from optimModels.optimization import evaluators, generators, replacers, variators, observers
from optimModels.simulation.simul_problems import KineticSimulationProblem
from optimModels.utils.constantes import optimType

class EAConfigurations():
    def __init__(self):
       # Configuration of EA algorithm
        self.MAX_GENERATIONS = 250
        self.POPULATION_SIZE = 100
        self.MAX_CANDIDATE_SIZE = 5
        self.POPULATION_SELECTED_SIZE = 50
        self.NUM_ELITES = 1
        self.CROSSOVER_RATE = 0.9
        self.MUTATION_RATE = 0.1
        self.NEW_CANDIDATES_RATE = 0.1
        self.TOURNAMENT_SIZE = 3
        self.NUM_CPUS = 2
        self.NUM_BEST_SOLUTIONS = 2

    def get_default_config(self):
        return [self.POPULATION_SIZE, self.MAX_CANDIDATE_SIZE, self.CROSSOVER_RATE,
                self.MUTATION_RATE, self.NEW_CANDIDATES_RATE, self.NUM_ELITES]


class OptimProblemConfiguration():
    """
    This class contains all information to perform a strain optimization

    Attributes
    -----------
    simulProblem : KineticSimulationProblem
        Configuration of a kinetic simulation problem (model and modifications over the parameters)
    decoder : an instance of decoderKnockouts or decoderUnderOverExpression class
        Responsible to convert a set of integers (int set representation) or a set of tuples (tuples of 2 integers) to knockouts or under/over levels of enzymes expression.
    evaluationFunc : an instance of targetFlux or BCPY class
        Function to calculate the fitness value of each candidate during the optimization process.
    EAConfiguration : configuration of evolutionary anlgorithms
    """
    def __init__(self, simulationProblem=None, type = None, decoder=None, evaluationFunc=None, EAConfig = None):
        if simulationProblem is None or type is None or decoder is None or evaluationFunc is None:
            raise Exception("You must give all the arguments!")
        self.simulProblem = simulationProblem
        self.type = type
        self.decoder = decoder
        self.evaluationFunc = evaluationFunc

        if EAConfig:
            self.EAConfig = EAConfig
        else:
            self.EAConfig = EAConfigurations()

    def get_simulation_problem(self):
        return self.simulProblem

    def get_number_reactions(self):
        return len(self.simulProblem.get_model().reactions)

    def get_decoder(self):
        return self.decoder

    def get_evaluation_function(self):
        return self.evaluationFunc

    def get_ea_configurations(self):
        return self.EAConfig

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


def run_optimization(optimProbConf, resultFile= None, isMultiProc=False, population = None):
    """
    Function to perform the optimization using the integer set representation to the candidates solutions.

    Parameters
    ----------
    optimProbConf : an instance of optimProblemConfiguration.
        This object contains all information to perform the strain optimization task.
    resultFile : str
        The path file to store all the results obtained during the optimization (default results are not saved into a file)
    isMultiProc : boolean value.
        True, if the user wants parallelize the population evaluation. (default False)

    Returns
    --------
    out : list of individuals
        The function returns the last population of EA.

    """
    #TODO consider the initial poputalion

    rand = Random()
    my_ec = ec.EvolutionaryComputation(rand)
    my_ec.selector = ec.selectors.tournament_selection
    my_ec.replacer = replacers.new_candidates_no_duplicates_replacement
    my_ec.terminator = ec.terminators.generation_termination

    if resultFile is not None:
        my_ec.observer = observers.save_all_results

    if optimProbConf.type in [optimType.REACTION_KO, optimType.GENE_KO, optimType.MEDIUM]:
        # ins set representation
        bounds = [0, len(optimProbConf.get_decoder().ids) - 1]
        myGenerator = generators.generator_single_int_set
        my_ec.variator = [variators.uniform_crossover,
                          variators.grow_mutation_intSetRep,
                          variators.shrink_mutation,
                          variators.single_mutation_intSetRep]
    elif optimProbConf.type == optimType.MEDIUM_REACTION_KO:
        bounds = [[0, 0], [len(optimProbConf.get_decoder().drains) - 1, len(optimProbConf.get_decoder().reactions) - 1]]
        myGenerator = generators.generator_tuple_int_set
        my_ec.variator = [variators.uniform_crossover_tuple,
                          variators.grow_mutation_tuple_intSetRep,
                          variators.shrink_mutation_tuple,
                          variators.single_mutation_tuple_intSetRep]
    else:
        #tuple set representation
        bounds = [[0, 0], [len(optimProbConf.get_decoder().ids) - 1, len(optimProbConf.get_decoder().levels) - 1]]
        myGenerator = generators.generator_single_int_tuple
        my_ec.variator = [variators.uniform_crossover_intTupleRep,
                          variators.grow_mutation_intTupleRep,
                          variators.shrink_mutation,
                          variators.single_mutation_intTupleRep]


    config = optimProbConf.get_ea_configurations()


    if isMultiProc:
        try:
            nprocs= int(cpu_count()/2)
        except NotImplementedError:
            nprocs = config.NUM_CPUS
        print("###########")
        nprocs=4
        print(nprocs)

        final_pop = my_ec.evolve(generator=myGenerator,
                                 evaluator=evaluators.parallel_evaluation_mp,
                                 mp_evaluator=evaluators.evaluator,
                                 mp_nprocs = nprocs,
                                 pop_size=config.POPULATION_SIZE,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 max_generations=config.MAX_GENERATIONS,
                                 candidate_max_size=config.MAX_CANDIDATE_SIZE,
                                 num_elites=config.NUM_ELITES,
                                 num_selected=config.POPULATION_SELECTED_SIZE,
                                 crossover_rate=config.CROSSOVER_RATE,
                                 mutation_rate=config.MUTATION_RATE,
                                 new_candidates_rate=config.NEW_CANDIDATES_RATE,
                                 configuration=optimProbConf,
                                 results_file=resultFile,
                                 tournament_size=config.TOURNAMENT_SIZE)
    else:
        final_pop = my_ec.evolve(generator=myGenerator,
                                 evaluator=evaluators.evaluator,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 pop_size=config.POPULATION_SIZE,
                                 max_generations=config.MAX_GENERATIONS,
                                 candidate_max_size=config.MAX_CANDIDATE_SIZE,
                                 num_elites=config.NUM_ELITES,
                                 num_selected=config.POPULATION_SELECTED_SIZE,
                                 crossover_rate=config.CROSSOVER_RATE,
                                 mutation_rate=config.MUTATION_RATE,
                                 new_candidates_rate=config.NEW_CANDIDATES_RATE,
                                 configuration=optimProbConf,
                                 results_file=resultFile,
                                 tournament_size=config.TOURNAMENT_SIZE
                                 )
    return final_pop







