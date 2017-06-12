from random import Random
from multiprocessing import cpu_count
from inspyred import ec
from collections import OrderedDict



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
        Responsible to convet a set of integers (int set representation) or a set of tuples (tuples of 2 integers) to knockouts or under/over levels of enzymes expression.
    objectiveFunc : an instance of targetFlux or BCPY class
        Function to calculate the fitness value of each candidate during the optimization process
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


def optimization_intSetRep(confOptimProblem, resultFile, isMultiProc=False):
    """
    Function to perform the optimization using the integer set representation to the candidates solutions.

    Parameters
    -----------
    confOptimProblem : an instance of optimProblemConfiguration
    bounds : minimum and maximum integer value allowed for


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
    my_ec.observer = observers.save_all_results

    bounds = [0, len(confOptimProblem.get_decoder().ids) - 1]
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
                                 configuration=confOptimProblem,
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
                                 configuration=confOptimProblem,
                                 results_file=resultFile,
                                 tournament_size=EAConfigurations.TOURNAMENT_SIZE
                                 )

    best_solutions = findBestSolutions(final_pop)

    return best_solutions


def optimization_tupleSetRep(confOptimProblem, resultFile, isMultiProc=False):
    rand = Random()
    my_ec = ec.EvolutionaryComputation(rand)
    my_ec.selector = ec.selectors.tournament_selection
    my_ec.variator = [variators.uniform_crossover,
                      variators.grow_mutation_intTupleRep,
                      variators.shrink_mutation,
                      variators.single_mutation_intTupleRep]
    my_ec.replacer = replacers.new_candidates_no_duplicates_replacement
    my_ec.terminator = ec.terminators.generation_termination
    my_ec.observer = observers.save_all_results

    bounds = [[0, 0], [len(confOptimProblem.get_decoder().ids) - 1, len(confOptimProblem.get_decoder().levels) - 1]]

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
                                 configuration=confOptimProblem,
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
                                 configuration=confOptimProblem,
                                 results_file=resultFile,
                                 tournament_size=EAConfigurations.TOURNAMENT_SIZE)


    best_solutions= findBestSolutions(final_pop)

    return best_solutions

def findBestSolutions(population):
    """
    Function to get the best individuals of a populations according to their fitness value. The number of individuals
    to return is given by  EAConfigurations.NUM_BEST_SOLUTIONS parameter.

    Parameters
    ------------
    population : list of individuals returned by EA

    Returns
    --------
    out : list of best individuals
    """
    bestPop = {}
    bestFitnessOrder = [-1] * EAConfigurations.NUM_BEST_SOLUTIONS
    minFitness = -1

    for ind in population:
        if ind.fitness > minFitness:
            minFitness = ind.fitness
            bestFitnessOrder.sort(reverse=True)
            toRem = bestFitnessOrder.pop()
            bestFitnessOrder.append(ind.fitness)
            if len(bestPop) >= EAConfigurations.NUM_BEST_SOLUTIONS:
                del bestPop[toRem]
            bestPop[ind.fitness] = ind

    return bestPop.values()

