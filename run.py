# -*- coding: utf-8 -*-

import sys
from os.path import dirname, join

sys.path.insert(0, join(dirname(__file__), "src"))

from optimModels.model.dynamicModel import load_kinetic_model
from optimModels.optimization.decoders import (
    decoderReactionsKnockouts, decoderUnderOverExpression)
from optimModels.optimization.evolutionaryComputation import (
    optimization_intSetRep, optimization_tupleSetRep, optimProblemConfiguration)
from optimModels.optimization.objectiveFunctions import targetFlux
from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver


def ko_chassagnole(sbml_file, filename, isMultiProc=False):
    model = load_kinetic_model(sbml_file)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1 / 3600},
            tSteps=[0, 1e9])
    res = problem.simulate(odeSolver.LSODA)
    print "Serine in WT ....."
    print res.get_fluxes_distribution()['vsersynth']

    reactionsToManipulate =['vPTS', 'vPGI', 'vPGM', 'vG6PDH', 'vPFK', 'vTA',
            'vTKA', 'vTKB', 'vMURSyNTH', 'vALDO', 'vGAPDH', 'vTIS', 'vTRPSYNTH',
            'vG3PDH', 'vPGK', 'vsersynth', 'vrpGluMu', 'vENO', 'vPK',
            'vpepCxylase', 'vSynth1', 'vSynth2', 'vDAHPS', 'vPDH', 'vMethSynth',
            'vPGDH', 'vR5PI', 'vRu5P', 'vPPK', 'vG1PAT']

    print reactionsToManipulate


    prob = optimProblemConfiguration(problem,
            decoder=decoderReactionsKnockouts(reactionsToManipulate),
            objectiveFunc=targetFlux("vsersynth"), solverId=odeSolver.LSODA)


    prob.set_optim_parameters(popSize=100, maxGenerations=10,
            popSelectedSize=50, maxCandidateSize=5, crossoverRate=1.0,
            mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [0, len(reactionsToManipulate) - 1]

    optimization_intSetRep(prob, bounds, filename, isMultiProc=isMultiProc)


if __name__ == '__main__':
    import time
    import warnings
    warnings.filterwarnings('ignore')  # ignore the warnings related to floating points raise from solver!!!
    t1 = time.time()
    ko_chassagnole("../Models/chassagnole2002.xml",
            "../SimulationResults/optim_chassagnole2002_serine_size5.csv", True)
    t2 = time.time()
#    t3 = time.time()
#    #underover_chassagnole(True)
#    t4 = time.time()
    print "time for 10 generations without multiproccessing" + str(t2 - t1)
#    print "time for 10 generations with multiproccessing 904 - " + str(t4 - t3)
    # underover_chassagnole()
