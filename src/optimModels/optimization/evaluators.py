"""
    ===============================================================
    :mod:`evaluators` -- evaluation of candidates
    ===============================================================
    .. module:: evaluators
    .. moduleauthor:: Sara Correia <sarag.correia@gmail.com>
"""
import math
import os
from optimModels.utils.constantes import solverStatus,Parameter

def evaluator(candidates, args):
    #print "--------- INITEVALUATION-------------"
    config = args["configuration"]
    decoder = config.get_decoder()
    simulProblem = config.get_simulation_problem()
    fitness = []
    solutions = []
    for candidate in candidates:
        overrideProblem = decoder.get_override_simul_problem(candidate, simulProblem)
        fitInd = -1.0
        try:
            res = simulProblem.simulate(config.get_solver_id(), overrideProblem)
            if res.get_solver_status() == solverStatus.OPTIMAL:
                fitInd = config.get_objective_function().get_fitness(res)
                if math.isnan(fitInd):
                    fitInd = 0.0

        except ValueError, e:
            print "Oops! Solver problems.  " + e.message
        solutions.append(decoder.candidate_decoded(candidate))
        fitness.append(fitInd)

    #print "---------EVALUATION-------------"
    #print "thread ID : " + str(os.getpid()) + "\n"+ str(candidates)+ "\n"+ str(fitness)
    #print "---------END EVALUATION-------------"
    return fitness
