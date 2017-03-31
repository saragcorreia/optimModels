"""
    =================================================================================
    :mod:`` -- optimization of Metabolic Models using Evolutinary Computation
    =================================================================================

    This module provides the framework for metabolic models optimization.

    .. Copyright 2016 Sara Correia
    .. module:: optimization
    .. moduleauthor:: Sara Correia <sarag.correia@gmail.com>
"""

from random import Random
from multiprocessing import cpu_count
from inspyred import ec
from optimModels.optimization import evaluators, generators, replacers, variators
from optimModels.optimization import observers


class optimProblemConfiguration():
    def __init__(self, simulationProblem=None, decoder=None, objectiveFunc=None, solverId=None):
        if objectiveFunc is None or solverId is None:
            raise Exception("You must indicate the objective function and the solver id.")
        self.simulProblem = simulationProblem
        self.decoder = decoder
        self.objectiveFunc = objectiveFunc
        self.solverId = solverId

    def get_simulation_problem(self):
        return self.simulProblem

    def get_number_reactions(self):
        return len(self.simulProblem.get_model().reactions)

    def get_decoder(self):
        return self.decoder

    def set_knockouts(self, ko_list):
        self.simulProblem.set_reactions_ko(ko_list)

    def set_parameters(self, parameters):
        self.simulProblem.set_parameters(parameters)

    # return the first reaction to optimize (NOT FINAL VERSION)
    def get_objective_function(self):
        return self.objectiveFunc;

    def get_solver_id(self):
        return self.solverId

    # set and gets of basic optimization problem parameters
    def set_optim_parameters(self, popSize=100, maxGenerations=100, popSelectedSize=50, maxCandidateSize=10,
                             numElites=1, crossoverRate=0.9, mutationRate=0.1, newCandidatesRate=0.1):
        self._populationSize = popSize
        self._maxGenerations = maxGenerations
        self._populationSelectedSize = popSelectedSize
        self._maxCandidateSize = maxCandidateSize
        self._numElites = numElites
        self._crossoverRate = crossoverRate
        self._mutationRate = mutationRate
        self._newCandidatesRate = newCandidatesRate

    @property
    def populationSize(self):
        return self._populationSize

    @populationSize.setter
    def populationSize(self, value):
        if type(value) is not int:
            raise TypeError("Population size must be an integer.")
        self._populationSize = value

    @property
    def maxGenerations(self):
        return self._maxGenerations

    @maxGenerations.setter
    def maxGenerations(self, value):
        if type(value) is not int:
            raise TypeError("Maximum number of generations must be an integer.")
        self._maxGenerations = value

    @property
    def maxCandidateSize(self):
        return self._maxCandidateSize

    @maxCandidateSize.setter
    def maxCandidateSize(self, value):
        if type(value) is not int:
            raise TypeError("Maximum of candidate size must be an integer.")
        self._maxCandidateSize = value

    @property
    def populationSelectedSize(self):
        return self._populationSelectedSize

    @populationSelectedSize.setter
    def populationSelectedSize(self, value):
        if type(value) is not int and value > self.population_size:
            raise TypeError(
                "Maximum candidates selected for variators must be an integer and lower than population size.")
        self._populationSelectedSize = value

    @property
    def numElites(self):
        return self._numElites

    @numElites.setter
    def numElites(self, value):
        if type(value) is not int:
            raise TypeError("Number of elites must be an integer.")
        self._numElites = value

    @property
    def crossoverRate(self):
        return self._crossoverRate

    @crossoverRate.setter
    def crossoverRate(self, value):
        if type(value) is not float or value < 0.0 or value > 1.0:
            raise ValueError("Crossover rate must be between 0 and 1.")
        self._crossoverRate = value

    @property
    def mutationRate(self):
        return self._mutationRate

    @mutationRate.setter
    def mutationRate(self, value):
        if type(value) is not float or value < 0.0 or value > 1.0:
            raise ValueError("Mutation rate must be between 0 and 1.")
        self._mutationRate = value

    @property
    def newCandidatesRate(self):
        return self._newCandidatesRate

    @newCandidatesRate.setter
    def newCandidatesRate(self, value):
        if type(value) is not float or value < 0.0 or value > 1.0:
            raise ValueError("New candidates rate must be between 0 and 1.")
        self._newCandidatesRate = value

    def get_parameters_str(self):
        params = [self.populationSize, self.maxCandidateSize, self.crossoverRate, self.mutationRate,
                  self.newCandidatesRate, self.numElites]
        return ";".join([str(elem) for elem in params]) + "\n"

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


def optimization_intSetRep(confOptimProblem, bounds, resultFile, isMultiProc=False):
    rand = Random()
    my_ec = ec.EvolutionaryComputation(rand)
    my_ec.selector = ec.selectors.tournament_selection
    ec.variators.arithmetic_crossover
    my_ec.variator = [variators.uniform_crossover,
                      variators.grow_mutation_intSetRep,
                      variators.shrink_mutation,
                      variators.single_mutation_intSetRep]

    my_ec.replacer = replacers.new_candidates_no_duplicates_replacement
    my_ec.terminator = ec.terminators.generation_termination
    my_ec.observer = observers.save_all_results

    # logger = logging.getLogger('inspyred.ec')
    # logger.setLevel(logging.DEBUG)
    # file_handler = logging.FileHandler('/Volumes/Data/inspyred.log', mode='w')
    # file_handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    if isMultiProc:
        print "Multiprocessing!!!"
        try:
            nprocs= int(cpu_count()/2)
        except NotImplementedError:
            nprocs = 10

        final_pop = my_ec.evolve(generator=generators.generator_intSetRep,
                                 evaluator=evaluators.parallel_evaluation_mp,
                                 mp_evaluator=evaluators.evaluator,
                                 mp_nprocs = nprocs,
                                 pop_size=confOptimProblem.populationSize,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 max_generations=confOptimProblem.maxGenerations,
                                 candidate_max_size=confOptimProblem.maxCandidateSize,
                                 num_elites=confOptimProblem.numElites,
                                 num_selected=confOptimProblem.populationSelectedSize,
                                 crossover_rate=confOptimProblem.crossoverRate,
                                 mutation_rate=confOptimProblem.mutationRate,
                                 new_candidates_rate=confOptimProblem.newCandidatesRate,
                                 configuration=confOptimProblem,
                                 results_file=resultFile,
                                 tournament_size=3)
    else:
        final_pop = my_ec.evolve(generator=generators.generator_intSetRep,
                                 evaluator=evaluators.evaluator,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 pop_size=confOptimProblem.populationSize,
                                 max_generations=confOptimProblem.maxGenerations,
                                 candidate_max_size=confOptimProblem.maxCandidateSize,
                                 num_elites=confOptimProblem.numElites,
                                 num_selected=confOptimProblem.populationSelectedSize,
                                 crossover_rate=confOptimProblem.crossoverRate,
                                 mutation_rate=confOptimProblem.mutationRate,
                                 new_candidates_rate=confOptimProblem.newCandidatesRate,
                                 configuration=confOptimProblem,
                                 results_file=resultFile,
                                 tournament_size=3
                                 )
    return final_pop


def optimization_tupleSetRep(confOptimProblem, bounds, resultFile, isMultiProc=False):
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

    # logger = logging.getLogger('inspyred.ec')
    # logger.setLevel(logging.DEBUG)
    # file_handler = logging.FileHandler('/Volumes/Data/inspyred.log', mode='w')
    # file_handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    if isMultiProc:
        print "Multiprocessing!!!"
        try:
            nprocs = int (cpu_count()/2)
        except NotImplementedError:
            nprocs = 10

        final_pop = my_ec.evolve(generator=generators.generator_intTupleRep,
                                 evaluator=evaluators.parallel_evaluation_mp,
                                 mp_evaluator=evaluators.evaluator,
                                 mp_nprocs=nprocs,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 pop_size=confOptimProblem.populationSize,
                                 max_generations=confOptimProblem.maxGenerations,
                                 candidate_max_size=confOptimProblem.maxCandidateSize,
                                 num_elites=confOptimProblem.numElites,
                                 num_selected=confOptimProblem.populationSelectedSize,
                                 crossover_rate=confOptimProblem.crossoverRate,
                                 mutation_rate=confOptimProblem.mutationRate,
                                 new_candidates_rate=confOptimProblem.newCandidatesRate,
                                 configuration=confOptimProblem,
                                 results_file=resultFile,
                                 tournament_size=3)
    else:
        final_pop = my_ec.evolve(generator=generators.generator_intTupleRep,
                                 evaluator=evaluators.evaluator,
                                 bounder=ec.Bounder(bounds[0], bounds[1]),
                                 pop_size=confOptimProblem.populationSize,
                                 max_generations=confOptimProblem.maxGenerations,
                                 candidate_max_size=confOptimProblem.maxCandidateSize,
                                 num_elites=confOptimProblem.numElites,
                                 num_selected=confOptimProblem.populationSelectedSize,
                                 crossover_rate=confOptimProblem.crossoverRate,
                                 mutation_rate=confOptimProblem.mutationRate,
                                 new_candidates_rate=confOptimProblem.newCandidatesRate,
                                 configuration=confOptimProblem,
                                 results_file=resultFile,
                                 tournament_size=3)
    return final_pop
