import copy

from optimModels.model.dynamicModel import load_kinetic_model
from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.optimization.decoders import decoderKnockouts,decoderUnderOverExpression
from optimModels.optimization.evolutionaryComputation import optimization_intSetRep,optimization_tupleSetRep,optimProblemConfiguration
from optimModels.utils.configurations import kineticConfigurations


def strain_optim(SBMLFile, objFunc=None, levels=None, criticalGenes=[], isMultiProc=False, resultFile=None):
    model = load_kinetic_model(SBMLFile)

    simulProblem = kineticSimulationProblem(model, tSteps=[0, kineticConfigurations.STEADY_STATE_TIME])

    # assumption: the reactionParamsAssociation obj : id_reac--> vMax_paramaeter. The critical Genes are identify by the vMax parameter name
    idsToManipulate = [x for x in simulProblem.model.reacParamsFactors.values() if x not in criticalGenes]
    idsToManipulate = sum(idsToManipulate, [])

    # build decoder
    if levels:
        decoder = decoderUnderOverExpression(idsToManipulate, levels)
    else:
        decoder = decoderKnockouts(idsToManipulate)

    #build optimization configuration problem
    prob = optimProblemConfiguration(simulProblem, decoder=decoder, objectiveFunc=objFunc, criticalGenes=criticalGenes)

    #run optimization
    if levels:
        best_solutions = optimization_tupleSetRep(prob, resultFile = resultFile, isMultiProc=isMultiProc)
    else:
        best_solutions = optimization_intSetRep(prob, resultFile = resultFile, isMultiProc=isMultiProc)

    #simplify solutions
    result = simplifySolutions(prob, best_solutions)

    return result



def simplifySolutions(confOptimProblem, population):
    simulProblem = confOptimProblem.get_simulation_problem()
    decoder = confOptimProblem.get_decoder()
    objFunction = confOptimProblem.get_objective_function()
    solutions = []

    for ind in population:
        overrideProblem = decoder.get_override_simul_problem(ind.candidate, simulProblem)
        fitness = ind.fitness

        factorsOrig = copy.copy(overrideProblem.get_factors())
        factorsFinal = copy.copy(overrideProblem.get_factors())

        # do not simplify solutions with fitness == 0 and with a single modification
        if fitness > 0.0 and len(factorsOrig) > 1:
            for k,v in factorsOrig.items():
                del factorsFinal[k]
                overrideProblem.set_factors(factorsFinal)

                try:
                    res = simulProblem.simulate(overrideProblem)
                    newFitness = objFunction.get_fitenss(res)
                except Exception:
                    newFitness = -1.0
                if round(fitness, 12) != round(newFitness, 12):
                    factorsFinal[k]=v

        print "simplify solutions"
        print factorsOrig
        print factorsFinal
        print "--------"
        overrideProblem.set_factors(factorsFinal)
        solutions.append(simulProblem.simulate(overrideProblem))
    return solutions