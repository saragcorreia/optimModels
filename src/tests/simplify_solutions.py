from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.utils.simplification import simplify_solutions

from optimModels.model.dynamicModel import load_kinetic_model

if __name__ == '__main__':
    dirResults = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/setEnzReactions/"
    sizes=[1,2,3,4,5,6,8,10]

    sbmlFile =  '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    #sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
    model = load_kinetic_model(sbmlFile)
    #dils = [(0.1)]
    dils = [(0.1/3600)]

    problem = kineticSimulationProblem(model, parameters={'Dil': dils[0]}, tSteps=[0, 1e9], timeout=100)

    for size in sizes:
        fileRes = dirResults + 'optim_Chassagnole_underover_Serine_size' + str(size) + '_True.csv'
        fileFinalRes = dirResults + 'Final_optim_Chassagnole_underover_Serine_size' + str(size) + '_True.csv'
        simplify_solutions(problem, fileRes, fileFinalRes, "vsersynth")
        #simplify_solutions(problem, fileRes, fileFinalRes, "vD_SUC")
