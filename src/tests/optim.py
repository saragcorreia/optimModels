from optimModels.optimization.decoders import decoderReactionsKnockouts, decoderUnderOverExpression
from optimModels.optimization.evolutionaryComputation import optimProblemConfiguration, optimization_intSetRep, \
    optimization_tupleSetRep
from optimModels.optimization.objectiveFunctions import targetFlux
from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver
from optimModels.model.dynamicModel import load_kinetic_model


def ko_chassagnole(isMultiProc=False):
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1 / 3600}, tSteps=[0, 1e9])
    res = problem.simulate(odeSolver.LSODA)
    print "Serine in WT ....."
    print res.get_fluxes_distribution()['vsersynth']

    reactionsToManipulate =['vPTS', 'vPGI', 'vPGM', 'vG6PDH', 'vPFK', 'vTA', 'vTKA', 'vTKB', 'vMURSyNTH', 'vALDO', 'vGAPDH', 'vTIS', 'vTRPSYNTH', 'vG3PDH', 'vPGK', 'vsersynth', 'vrpGluMu', 'vENO', 'vPK', 'vpepCxylase', 'vSynth1', 'vSynth2', 'vDAHPS', 'vPDH', 'vMethSynth', 'vPGDH', 'vR5PI', 'vRu5P', 'vPPK', 'vG1PAT']

    print reactionsToManipulate


    prob = optimProblemConfiguration(problem, decoder=decoderReactionsKnockouts(reactionsToManipulate),
                                     objectiveFunc=targetFlux("vsersynth"),
                                     solverId=odeSolver.LSODA)


    prob.set_optim_parameters(popSize=100, maxGenerations=10, popSelectedSize=50, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [0, len(reactionsToManipulate) - 1]

    optimization_intSetRep(prob, bounds,
                           "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Chassagnole_Serine_size5" + str(
                               isMultiProc) + ".csv",
                           isMultiProc=isMultiProc)


def underover_chassagnole(isMultiProc):
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1 / 3600}, tSteps=[0, 1e9])
    res = problem.simulate(odeSolver.LSODA)
    print "Serine in WT ...ko_chassagnole.."
    print res.get_fluxes_distribution()['vsersynth']

    reactionsToManipulate =['vPTS', 'vPGI', 'vPGM', 'vG6PDH', 'vPFK', 'vTA', 'vTKA', 'vTKB', 'vMURSyNTH', 'vALDO', 'vGAPDH', 'vTIS', 'vTRPSYNTH', 'vG3PDH', 'vPGK', 'vsersynth', 'vrpGluMu', 'vENO', 'vPK', 'vpepCxylase', 'vSynth1', 'vSynth2', 'vDAHPS', 'vPDH', 'vMethSynth', 'vPGDH', 'vR5PI', 'vRu5P', 'vPPK', 'vG1PAT']
    prob = optimProblemConfiguration(problem, decoder=decoderUnderOverExpression(reactionsToManipulate,levels),
                                     objectiveFunc=targetFlux("vsersynth"),
                                     solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=100, maxGenerations=10, popSelectedSize=50, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [[0, 0], [len(reactionsToManipulate) - 1, len(levels) - 1]]

    optimization_tupleSetRep(prob, bounds,
                             resultFile="/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Chassagnole_Serine_size5" + str(
                                 isMultiProc) + ".csv", isMultiProc=isMultiProc)


    #################
def ko_jahan(isMultiProc=False):
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1}, tSteps=[0, 1e9], timeout = 300)
    res = problem.simulate(odeSolver.LSODA)
    print "vD_SUC in WT ....."
    print res.get_fluxes_distribution()['vD_SUC']

    reactionsToManipulate = [x for x in model.reactions.keys() if "vD_" in x]
    prob = optimProblemConfiguration(problem, decoder=decoderReactionsKnockouts(reactionsToManipulate), objectiveFunc=targetFlux("vD_SUC"),
                                     solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=10, maxGenerations=10, popSelectedSize=5, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [0, len(reactionsToManipulate) - 1]

    final_pop = optimization_intSetRep(prob, bounds,
                                       "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Jahan_SUC_size5" + str(
                                           isMultiProc) + ".csv",
                                       isMultiProc=isMultiProc)


def underover_jahan(isMultiProc=False):
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1}, tSteps=[0, 1e9], timeout = 300)
    res = problem.simulate(odeSolver.LSODA)
    print "vD_SUC in WT ...."
    print res.get_fluxes_distribution()['vD_SUC']

    reactionsToManipulate = [x for x in model.reactions.keys() if "vD_" in x]
    prob = optimProblemConfiguration(problem, decoder=decoderUnderOverExpression(reactionsToManipulate,levels),
                                     objectiveFunc=targetFlux("vD_SUC"),
                                     solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=10, maxGenerations=10, popSelectedSize=5, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [[0, 0], [len(reactionsToManipulate) - 1, len(levels) - 1]]

    final_pop = optimization_tupleSetRep(prob, bounds,
                                         resultFile="/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Jahan_SUC_size5" + isMultiProc + ".csv",
                                         isMultiProc=isMultiProc)


if __name__ == '__main__':
    import time
    import warnings
    warnings.filterwarnings('ignore')  # ignore the warnings related to floating points raise from solver!!!
    t1 = time.time()
    ko_chassagnole(True)
    t2 = time.time()
    t3 = time.time()
    #underover_chassagnole(True)
    t4 = time.time()
    print "time for 10 generations without multiproccessing" + str(t2 - t1)
    print "time for 10 generations with multiproccessing 904 - " + str(t4 - t3)
    # underover_chassagnole()
