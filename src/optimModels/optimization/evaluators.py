"""
    ===============================================================
    :mod:`evaluators` -- evaluation of candidates
    ===============================================================



    .. module:: evaluators
    .. moduleauthor:: Sara Correia <sarag.correia@gmail.com>
"""
import math


def evaluator(candidates, args):
    config = args["configuration"]
    decoder = config.get_decoder()
    simulProblem = config.get_simulation_problem()
    fitness = []
    solutions = []
    for candidate in candidates:
        decoder.update_simulation_problem(candidate, simulProblem)
        fitInd = -1.0
        try:
            res = simulProblem.simulate(config.get_solver_id())
            fitInd = config.get_objective_function().get_fitness(res)
            if math.isnan(fitInd):
                fitInd = 0.0
        except ValueError, e:
            print "Oops! Solver problems.  " + e.message

        solutions.append(decoder.candidate_decoded(candidate, config.get_simulation_problem().model))
        fitness.append(fitInd)

    # print "---------EVALUATION-------------"
    # print candidates
    # print fitness
    # print "---------END EVALUATION-------------"
    return fitness
