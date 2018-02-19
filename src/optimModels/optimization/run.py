from collections import OrderedDict

from optimModels.optimization.observers import load_population
from optimModels.optimization.decoders import *
from optimModels.optimization.evolutionary_computation import run_optimization, OptimProblemConfiguration, \
    EAConfigurations
from optimModels.utils.constantes import optimType
from optimModels.utils.configurations import StoicConfigurations

import itertools


def cbm_strain_optim(simulProblem, evaluationFunc, levels, type=optimType.REACTION_KO, criticalReacs=[], isMultiProc=False, candidateSize = None,
                     resultFile=None, initPopFile=None):

    if type == optimType.MEDIUM or type == optimType.MEDIUM_LEVELS:
        idsToManipulate = [x for x in simulProblem.get_drains() if x not in criticalReacs and x not in simulProblem.objective.keys()]
    elif type == optimType.REACTION_KO or type == optimType.REACTION_UO:
        idsToManipulate = [x for x in simulProblem.get_internal_reactions() if x not in criticalReacs and x not in simulProblem.objective.keys()]
    elif type == optimType.MEDIUM_REACTION_KO:
        drainsToManipulate = [x for x in simulProblem.get_drains() if x not in criticalReacs and x not in simulProblem.objective.keys()]
        reacsToManipulate = [x for x in simulProblem.get_internal_reactions() if x not in criticalReacs and x not in simulProblem.objective.keys()]
    else:
        raise Exception("cbm_strain_optim:NOT IMMPLEMENTED!")


    # build decoder
    if type == optimType.REACTION_KO:
        decoder = DecoderReacKnockouts(idsToManipulate)
    elif type == optimType.REACTION_UO:
        if not levels:
            raise Exception("The specification of levels for under/over optimizarion is required!")
        decoder = DecoderReacUnderOverExpression(idsToManipulate, levels)
    elif type == optimType.MEDIUM:
        decoder = DecoderMedium(idsToManipulate)
    elif type == optimType.MEDIUM_LEVELS:
        if not levels:
            raise Exception("The specification of levels for teh optimizarion is required!")
        decoder = DecoderMediumLevels(idsToManipulate, levels)
    elif type == optimType.MEDIUM_REACTION_KO:
        decoder = DecoderMediumReacKO(drainsToManipulate, reacsToManipulate)

    initPopulation = None
    if initPopFile is not None:
        numGeneration, initPopulation = load_population(initPopFile, decoder)

    # build optimization configuration problem
    eaConfig = EAConfigurations()
    if candidateSize:
        eaConfig.MAX_CANDIDATE_SIZE = candidateSize;

    optimProbConf = OptimProblemConfiguration(simulProblem, type=type, decoder=decoder, evaluationFunc=evaluationFunc,
                                              EAConfig=eaConfig)

    # run optimization
    final_pop = run_optimization(optimProbConf, resultFile=resultFile, isMultiProc=isMultiProc,
                                 population=initPopulation)

    best_solutions = findBestSolutions(final_pop, eaConfig)

    # simplify solutions
    result = simplifySolutions(optimProbConf, best_solutions)

    print_results(resultFile,final_pop,optimProbConf )

    return result


def kinetic_strain_optim(simulProblem, objFunc=None, levels=None, criticalParameters=[], isMultiProc=False, candidateSize = None, resultFile=None,
                         initPopFile=None):
    """
    Function to perform the strain optimization using kinetic metabolic models.

    Parameters
    ----------
    simulProblem : SimulationProblem instance ( KineticSimulationProblem, StoicSimulationProblem).
    objFunc : objectiveFunction
        Function used to calculate the fitness value.
    levels : list of floats
        List of values that can be used to multiply by the vMax parameters in over/under expression enzymes levels.
    criticalParameters : list of str
        List of parameters identifiers which can not be manipulated.
    isMultiProc : boolean
        Boolean variable used to paralallize the evaluation of candidates.

    Returns
    -------
    out : list of kineticSimulationResults
        The function returns the best solutions found in strain optimization. The kineticSimulationResults object has the
        flux distribution and metabolites concentration at steady-state, and the modifications made over the
        original model.

    """

    # assumption: the reactionParamsAssociation obj : id_reac--> vMax_paramaeter. The critical Genes are identify by the vMax parameter name
    allParams = list(set(itertools.chain.from_iterable(simulProblem.model.reacParamsFactors.values())))
    idsToManipulate = [x for x in allParams if x not in criticalParameters]

    if type == optimType.REACTION_KO:
        decoder = DecoderReacKnockouts(idsToManipulate, levels)
    elif type == optimType.REACTION_UO:
        if not levels:
            raise Exception("The specification of levels for under/over optimizarion is required!")
        decoder = DecoderReacUnderOverExpression(idsToManipulate, levels)

    # load initial population from file
    initPopulation = None
    numGeneration = 0
    if initPopFile is not None:
        numGeneration, initPopulation = load_population(initPopFile, decoder)

    # build optimization configuration problem
    eaConfig = EAConfigurations()
    if candidateSize:
        eaConfig.MAX_CANDIDATE_SIZE = candidateSize;

    optimProbConf = OptimProblemConfiguration(simulProblem, type=type, decoder=decoder, evaluationFunc=objFunc,
                                              EAConfig=eaConfig)

    # run optimization
    final_pop = run_optimization(optimProbConf, type=type, resultFile=resultFile, isMultiProc=isMultiProc,
                                 population=initPopulation, nextGen=numGeneration)

    best_solutions = findBestSolutions(final_pop, eaConfig)

    # simplify solutions
    result = simplifySolutions(optimProbConf, best_solutions)

    print_results(resultFile,final_pop,optimProbConf )

    return result


def findBestSolutions(population, eaConfig):
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
    bestFitnessOrder = [-1] * eaConfig.NUM_BEST_SOLUTIONS
    minFitness = -1

    for ind in population:
        if ind.fitness > minFitness:
            minFitness = ind.fitness
            bestFitnessOrder.sort(reverse=True)
            toRem = bestFitnessOrder.pop()
            bestFitnessOrder.append(ind.fitness)
            if len(bestPop) >= eaConfig.NUM_BEST_SOLUTIONS:
                del bestPop[toRem]
            bestPop[ind.fitness] = ind

    return bestPop.values()


def simplifySolutions(optimProbConf, population):
    """
    This function removes the modifications (KO or under/expression of an enzyme) which not influence the fitness value of the candidate solution.

    Parameters
    -----------
    optimProbConf: an instance of optimProblemConfiguration
        The configuration problem.
    population: list of individuals
        List of individuals returned by EA algorithm.

    Returns
    -------
    out : list of kineticSimulationResults
        The function returns the best solutions found in strain optimization. The kineticSimulationResults object has the
        flux distribution and metabolites concentration at steady-state, and the modifications made over the
        original model.
    """
    simulProblem = optimProbConf.get_simulation_problem()
    decoder = optimProbConf.get_decoder()
    evalFunction = optimProbConf.get_evaluation_function()
    solutions = []

    for ind in population:
        overrideProblem = decoder.get_override_simul_problem(ind.candidate, simulProblem)
        fitness = ind.fitness

        # do not simplify solutions with fitness == 0 and with a single modification
        if fitness > 0.0 and len(overrideProblem.get_modifications()) > 1:
            overrideProblem.simplify_modifications(simulProblem, evalFunction, fitness)
        solutions.append(simulProblem.simulate(overrideProblem))
    return solutions

def print_results (fileName, population, optimConfig):

    file = open(fileName, 'a')
    file.write("population_size;candidate_max_size;crossover_rate; mutation_rate;new_candidates_rate; num_elites\n")
    file.write(";".join(map(str,optimConfig.get_ea_configurations().get_default_config())))
    file.write("Generation;Fitness;Candidate;Reactions\n")

    # save all candidates of the population
    for ind in population:
        solution_decoded = optimConfig.get_decoder().decode_candidate(ind.candidate)
        file.write(("{0};{1};{2};{3} \n").format("final", ind.fitness, ind.candidate, solution_decoded))
    file.close()