from optimModels.optimization.decoders import decoderReactionsKnockouts, decoderUnderOverExpression
from optimModels.optimization.evolutionaryComputation import optimProblemConfiguration, optimization_intSetRep, optimization_tupleSetRep
from optimModels.optimization.objectiveFunctions import targetFlux
from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver
from optimModels.model.dynamicModel import load_kinetic_model


def ko_chassagnole ():
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1/3600}, tSteps=[0, 1e9])
    res = problem.simulate(odeSolver.LSODA)
    print "Serine in WT ....."
    print res.get_fluxes_distribution()['vsersynth']

    prob = optimProblemConfiguration(problem, decoder=decoderReactionsKnockouts(),
                                     objectiveFunc=targetFlux("vsersynth"),
                                     solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=100, maxGenerations=10, popSelectedSize=50, maxCandidateSize=8,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [0, problem.get_number_reactions() - 1]

    final_pop = optimization_intSetRep(prob, bounds,
                                       resultFile="/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Chassagnole_Serine_size8.csv")


def underover_chassagnole():
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1/3600}, tSteps=[0, 1e9])
    res = problem.simulate( odeSolver.LSODA)
    print "Serine in WT ...ko_chassagnole.."
    print res.get_fluxes_distribution()['vsersynth']

    prob = optimProblemConfiguration(problem, decoder=decoderUnderOverExpression(levels),
                                     objectiveFunc=targetFlux("vsersynth"),
                                     solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=10, maxGenerations=10, popSelectedSize=5, maxCandidateSize=8,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [[0, 0], [problem.get_number_reactions() - 1, len(levels) - 1]]

    final_pop = optimization_tupleSetRep(prob, bounds,
                                       resultFile="/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Chassagnole_Serine_size8.csv")

if __name__ == '__main__':
    #ko_chassagnole()
    underover_chassagnole()