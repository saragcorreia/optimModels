from optimModels.optimization.decoders import decoderReactionsKnockouts, decoderUnderOverExpression
from optimModels.optimization.evolutionaryComputation import optimProblemConfiguration, optimization_intSetRep, optimization_tupleSetRep
from optimModels.optimization.objectiveFunctions import targetFlux
from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver
from optimModels.model.dynamicModel import load_kinetic_model


def ko_chassagnole (multiprocessing = False):
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1/3600}, tSteps=[0, 1e9])
    res = problem.simulate(odeSolver.LSODA)
    print "Serine in WT ....."
    print res.get_fluxes_distribution()['vsersynth']

    prob = optimProblemConfiguration(problem, decoder=decoderReactionsKnockouts(),
                                     objectiveFunc=targetFlux("vsersynth"),
                                     solverId=odeSolver.LSODA)

    prob = optimProblemConfiguration(problem, decoder=decoderReactionsKnockouts(), objectiveFunc=targetFlux("vsersynth"),solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=100, maxGenerations=10, popSelectedSize=50, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [0, problem.get_number_reactions() - 1]

    final_pop = optimization_intSetRep(prob, bounds, "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Chassagnole_Serine_size5"+str(multiprocessing)+".csv",
                                       multiprocessing = multiprocessing)


def underover_chassagnole():
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1/3600}, tSteps=[0, 1e9])
    res = problem.simulate( odeSolver.LSODA)
    print "Serine in WT ...ko_chassagnole.."
    print res.get_fluxes_distribution()['vsersynth']

    #prob = optimProblemConfiguration(problem, decoder=decoderUnderOverExpression(levels),
    #                                 objectiveFunc=targetFlux("vsersynth"),
    #                                 solverId=odeSolver.LSODA)

    prob = optimProblemConfiguration(solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=100, maxGenerations=10, popSelectedSize=50, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [[0, 0], [problem.get_number_reactions() - 1, len(levels) - 1]]

    final_pop = optimization_tupleSetRep(prob, bounds,
                                       resultFile="/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Chassagnole_Serine_size5.csv")


#################

def ko_jahan (multiprocessing = False):
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1}, tSteps=[0, 1e9])
    res = problem.simulate(odeSolver.LSODA)
    print "vD_SUC in WT ....."
    print res.get_fluxes_distribution()['vD_SUC']

    prob = optimProblemConfiguration(problem, decoder=decoderReactionsKnockouts(),
                                     objectiveFunc=targetFlux("vD_SUC"),
                                     solverId=odeSolver.LSODA)

    prob = optimProblemConfiguration(problem, decoder=decoderReactionsKnockouts(), objectiveFunc=targetFlux("vD_SUC"),solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=100, maxGenerations=10, popSelectedSize=50, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [0, problem.get_number_reactions() - 1]

    final_pop = optimization_intSetRep(prob, bounds, "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Jahan_SUC_size5"+str(multiprocessing)+".csv",
                                       multiprocessing = multiprocessing)


def underover_jahan():
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1}, tSteps=[0, 1e9])
    res = problem.simulate( odeSolver.LSODA)
    print "vD_SUC in WT ...."
    print res.get_fluxes_distribution()['vD_SUC']

    #prob = optimProblemConfiguration(problem, decoder=decoderUnderOverExpression(levels),
    #                                 objectiveFunc=targetFlux("vsersynth"),
    #                                 solverId=odeSolver.LSODA)

    prob = optimProblemConfiguration(solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=100, maxGenerations=10, popSelectedSize=50, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [[0, 0], [problem.get_number_reactions() - 1, len(levels) - 1]]

    final_pop = optimization_tupleSetRep(prob, bounds,
                                       resultFile="/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Jahan_SUC_size5.csv")




if __name__ == '__main__':
    import time
    t1 = time.time()
    ko_jahan(False)
    t2 = time.time()
    print "time for 10 generations without multiproccessing" + str(t2-t1)

    t1 = time.time()
    ko_jahan(True)
    t2 = time.time()
    print "time for 10 generations with multiproccessing" + str(t2 - t1)

    #underover_chassagnole()