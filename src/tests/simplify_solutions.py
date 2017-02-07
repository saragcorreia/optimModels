from optimModels.simulation.simulationProblems import KineticSimulationProblem
from optimModels.utils.simplification import simplify_solutions

from src.optimModels.model.dynamicModel import load_kinetic_model

if __name__ == '__main__':
    dirResults = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/"
    sizes=[1,2,3,4,5,6]

    sbmlFile =  '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)
    dils = [(0.1/3600)]

    problem = KineticSimulationProblem(model, parameters={'Dil': dils[0]}, tSteps=[0, 1e9])
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]

    for size in sizes:
        fileRes = dirResults + 'optim_Chassagnole_Serine_size' + str(size) + '.csv'
        fileFinalRes = dirResults + 'Final_optim_Chassagnole_Serine_size' + str(size) + '.csv'
        simplify_solutions(problem, fileRes, fileFinalRes, "vsersynth")
