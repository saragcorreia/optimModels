# -*- coding: utf-8 -*-

import sys
from os.path import dirname, join

sys.path.insert(0, join(dirname(__file__), "src"))

from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.utils.simplification import simplify_solutions
from optimModels.model.dynamicModel import load_kinetic_model

if __name__ == '__main__':
    dirResults = "../SimulationResults/"
    sizes=[1,2,3,4,5,6]

    sbmlFile =  '../Models/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)
    dils = [(0.1/3600)]

    problem = kineticSimulationProblem(model, parameters={'Dil': dils[0]}, tSteps=[0, 1e9])
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]

    for size in sizes:
        fileRes = dirResults + 'optim_Chassagnole_Serine_size' + str(size) + '.csv'
        fileFinalRes = dirResults + 'Final_optim_Chassagnole_Serine_size' + str(size) + '.csv'
        simplify_solutions(problem, fileRes, fileFinalRes, "vsersynth")
