from collections import OrderedDict


from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.optimization.observers import load_population
from optimModels.optimization.decoders import decoderKnockouts,decoderUnderOverExpression
from optimModels.optimization.evolutionaryComputation import optimization_intSetRep,optimization_tupleSetRep,optimProblemConfiguration
from optimModels.utils.configurations import kineticConfigurations
from optimModels.utils.configurations import EAConfigurations
import itertools

def strain_optim(model, objFunc=None, levels=None, criticalGenes=[], isMultiProc=False, resultFile=None, initPopFile = None):
    """
    Function to perform the strain optimization using kinetic metabolic models.

    Parameters
    ----------
    model : kineticModel
        The kinetic metabolic model.
    objFunc : objectiveFunction
        Function used to calculate the fitness value.
    levels : list of floats
        List of values that can be used to multiply by the vMax parameters in over/under expression enzymes levels.
    criticalGenes : list of str
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
    simulProblem = kineticSimulationProblem(model, tSteps=[0, kineticConfigurations.STEADY_STATE_TIME])

    # assumption: the reactionParamsAssociation obj : id_reac--> vMax_paramaeter. The critical Genes are identify by the vMax parameter name
    allParams = list(set(itertools.chain.from_iterable(simulProblem.model.reacParamsFactors.values())))
    idsToManipulate = [x for x in allParams if x not in criticalGenes]

    # build decoder
    if levels:
        decoder = decoderUnderOverExpression(idsToManipulate, levels)
    else:
        decoder = decoderKnockouts(idsToManipulate)

    #load initial population from file
    initPopulation = None
    numGeneration = 0
    if initPopFile is not None:
        numGeneration, initPopulation = load_population(initPopFile, decoder)

    #build optimization configuration problem
    optimProbConf = optimProblemConfiguration(simulProblem, decoder=decoder, objectiveFunc=objFunc, criticalGenes=criticalGenes)

    #run optimization
    if levels:
        final_pop = optimization_tupleSetRep(optimProbConf, resultFile = resultFile, isMultiProc=isMultiProc, population = initPopulation, nextGen = numGeneration)
    else:
        final_pop = optimization_intSetRep(optimProbConf, resultFile = resultFile, isMultiProc=isMultiProc, population = initPopulation, nextGen = numGeneration)


    best_solutions = findBestSolutions(final_pop)

    #simplify solutions
    result = simplifySolutions(optimProbConf, best_solutions)

    return result

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
    objFunction = optimProbConf.get_objective_function()
    solutions = []

    for ind in population:
        overrideProblem = decoder.get_override_simul_problem(ind.candidate, simulProblem)

        fitness = ind.fitness

        factorsOrig = OrderedDict(overrideProblem.get_factors())
        factorsFinal = OrderedDict(overrideProblem.get_factors())

        # do not simplify solutions with fitness == 0 and with a single modification
        if fitness > 0.0 and len(factorsOrig) > 1:
            for k,v in factorsOrig.items():
                del factorsFinal[k]
                overrideProblem.set_factors(factorsFinal)

                try:
                    res = simulProblem.simulate(overrideProblem)
                    print (objFunction.get_name())

                    newFitness = objFunction.get_fitness(res)
                except Exception:
                    newFitness = -1.0

                print (fitness)
                print (newFitness)
                if round(fitness, 12) != round(newFitness, 12):
                    factorsFinal[k]=v

        print ("simplify solutions")
        print (factorsOrig)
        print (factorsFinal)
        print ("--------")
        overrideProblem.set_factors(factorsFinal)
        solutions.append(simulProblem.simulate(overrideProblem))
    return solutions