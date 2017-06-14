from random import Random
from multiprocessing import cpu_count
from inspyred import ec

from optimModels.optimization import evaluators, generators, replacers, variators, observers
from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.utils.configurations import EAConfigurations



class optimProblemConfiguration():
    """
    This class contains all information to perform a strain optimization

    Attributes
    ------------
    simulProblem : kineticSimulationProblem
        Configuration of a kinetic simulation problem (model and modifications over the parameters)
    decoder : an instance of decoderKnockouts or decoderUnderOverExpression class
        Responsible to convert a set of integers (int set representation) or a set of tuples (tuples of 2 integers) to knockouts or under/over levels of enzymes expression.
    objectiveFunc : an instance of targetFlux or BCPY class
        Function to calculate the fitness value of each candidate during the optimization process.
    criticalGenes: set of str
        Set of parameters that can not be manipulated during the optimization process.
    """
    def __init__(self, simulationProblem=None, decoder=None, objectiveFunc=None, criticalGenes = None):
        if simulationProblem is None or decoder is None or objectiveFunc is None:
            raise Exception("You must give all the arguments!")
        self.simulProblem = simulationProblem
        self.decoder = decoder
        self.objectiveFunc = objectiveFunc
        self.criticalGenes = criticalGenes

    def get_simulation_problem(self):
        return self.simulProblem

    def get_number_reactions(self):
        return len(self.simulProblem.get_model().reactions)

    def get_decoder(self):
        return self.decoder

    def get_objective_function(self):
        return self.objectiveFunc;

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


def optimization_intSetRep(optimProbConf, resultFile= None, isMultiProc=False):
    """
    Function to perform the optimization using the integer set representation to the candidates solutions.

    Parameters
    -----------
    optimProbConf : an instance of optimProblemConfiguration.
        This object contains all information to perform the strain optimization task.
    resultFile : str
        The path file to store all the results obtained during the optimization (default results are not saved into a file)
    isMultiProc : boolean value.
        True, if the user wants parallelize the population evaluation. (default False)

    Returns
    ---------
    out : list of individuals
        The function returns the last population of EA.

    """
    rand = Random()
    my_ec = ec.EvolutionaryComputation(rand)
    my_ec.selector = ec.selectors.tournament_selection
    my_ec.variator = [variators.uniform_crossover,
                      variators.grow_mutation_intSetRep,
                      variators.shrink_mutation,
                      variators.single_mutation_intSetRep]

    my_ec.replacer = replacers.new_candidates_no_duplicates_replacement
    my_ec.terminator = ec.terminators.generation_termination

    if resultFile is not None:
        my_ec.observer = observers.save_all_results

    bounds = [0, len(optimProbConf.get_decoder().ids) - 1]
    if isMultiProc:
        try:
            nprocs= int(cpu_count()/2)
        except NotImplementedError:
            nprocs = EAConfigurations.NUM_CPUS

        final_pop = my_ec.evolve(generator=generators.generator_intSetRep,
                                 evaluator=evaluators.parallel_evaluation_mp,
                                 mp_evaluator=evaluators.evaluator,
                                 mp_nprocs = nprocs,
                                 pop_size=EAConfigurations.POPULATION_SIZE,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 max_generations=EAConfigurations.MAX_GENERATIONS,
                                 candidate_max_size=EAConfigurations.MAX_CANDIDATE_SIZE,
                                 num_elites=EAConfigurations.NUM_ELITES,
                                 num_selected=EAConfigurations.POPULATION_SELECTED_SIZE,
                                 crossover_rate=EAConfigurations.CROSSOVER_RATE,
                                 mutation_rate=EAConfigurations.MUTATION_RATE,
                                 new_candidates_rate=EAConfigurations.NEW_CANDIDATES_RATE,
                                 configuration=optimProbConf,
                                 results_file=resultFile,
                                 tournament_size=EAConfigurations.TOURNAMENT_SIZE)
    else:
        final_pop = my_ec.evolve(generator=generators.generator_intSetRep,
                                 evaluator=evaluators.evaluator,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 pop_size=EAConfigurations.POPULATION_SIZE,
                                 max_generations=EAConfigurations.MAX_GENERATIONS,
                                 candidate_max_size=EAConfigurations.MAX_CANDIDATE_SIZE,
                                 num_elites=EAConfigurations.NUM_ELITES,
                                 num_selected=EAConfigurations.POPULATION_SELECTED_SIZE,
                                 crossover_rate=EAConfigurations.CROSSOVER_RATE,
                                 mutation_rate=EAConfigurations.MUTATION_RATE,
                                 new_candidates_rate=EAConfigurations.NEW_CANDIDATES_RATE,
                                 configuration=optimProbConf,
                                 results_file=resultFile,
                                 tournament_size=EAConfigurations.TOURNAMENT_SIZE
                                 )
    return final_pop


def optimization_tupleSetRep(optimProbConf, resultFile= None, isMultiProc=False):
    """
    Function to perform the optimization using the tuple set representation to the candidates solutions.

    Parameters
    -----------
    optimProbConf : an instance of optimProblemConfiguration.
        This object contains all information to perform the strain optimization task.
    resultFile : str
        The path file to store all the results obtained during the optimization (default results are not saved into a file)
    isMultiProc : boolean value.
        True, if the user wants parallelize the population evaluation. (default False)

    Returns
    ---------
    out : list of individuals
        The function returns the last population of EA.


    """
    rand = Random()
    my_ec = ec.EvolutionaryComputation(rand)
    my_ec.selector = ec.selectors.tournament_selection
    my_ec.variator = [variators.uniform_crossover,
                      variators.grow_mutation_intTupleRep,
                      variators.shrink_mutation,
                      variators.single_mutation_intTupleRep]
    my_ec.replacer = replacers.new_candidates_no_duplicates_replacement
    my_ec.terminator = ec.terminators.generation_termination
    if resultFile is not None:
        my_ec.observer = observers.save_all_results


    bounds = [[0, 0], [len(optimProbConf.get_decoder().ids) - 1, len(optimProbConf.get_decoder().levels) - 1]]

    if isMultiProc:
        try:
            nprocs = int (cpu_count()/2)
        except NotImplementedError:
            nprocs  = EAConfigurations.NUM_CPUS

        final_pop = my_ec.evolve(generator=generators.generator_intTupleRep,
                                 evaluator=evaluators.parallel_evaluation_mp,
                                 mp_evaluator=evaluators.evaluator,
                                 mp_nprocs=nprocs,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 pop_size=EAConfigurations.POPULATION_SIZE,
                                 max_generations=EAConfigurations.MAX_GENERATIONS,
                                 candidate_max_size=EAConfigurations.MAX_CANDIDATE_SIZE,
                                 num_elites=EAConfigurations.NUM_ELITES,
                                 num_selected=EAConfigurations.POPULATION_SELECTED_SIZE,
                                 crossover_rate=EAConfigurations.CROSSOVER_RATE,
                                 mutation_rate=EAConfigurations.MUTATION_RATE,
                                 new_candidates_rate=EAConfigurations.NEW_CANDIDATES_RATE,
                                 configuration=optimProbConf,
                                 results_file=resultFile,
                                 tournament_size=EAConfigurations.TOURNAMENT_SIZE)
    else:
        final_pop = my_ec.evolve(generator=generators.generator_intTupleRep,
                                 evaluator=evaluators.evaluator,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 pop_size=EAConfigurations.POPULATION_SIZE,
                                 max_generations=EAConfigurations.MAX_GENERATIONS,
                                 candidate_max_size=EAConfigurations.MAX_CANDIDATE_SIZE,
                                 num_elites=EAConfigurations.NUM_ELITES,
                                 num_selected=EAConfigurations.POPULATION_SELECTED_SIZE,
                                 crossover_rate=EAConfigurations.CROSSOVER_RATE,
                                 mutation_rate=EAConfigurations.MUTATION_RATE,
                                 new_candidates_rate=EAConfigurations.NEW_CANDIDATES_RATE,
                                 configuration=optimProbConf,
                                 results_file=resultFile,
                                 tournament_size=EAConfigurations.TOURNAMENT_SIZE)

    return final_pop



