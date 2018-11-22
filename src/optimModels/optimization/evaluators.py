
import math
import logging
import time
from optimModels.utils.constantes import solverStatus
from optimModels.utils.utils import MyPool

try:
    import cPickle as pickle
except ImportError:
    import pickle

def evaluator(candidates, args):
    """
    This function allows the evaluation of candidate solutions.

    Args:
        candidates (list): A list of candidate solutions
        args (dict): A dictionary of keyword arguments

    Returns:
        list of floats: a list of fitness values
    """

    config = args["configuration"]
    decoder = config.get_decoder()
    simulProblem = config.get_simulation_problem()
    fitness = []
    for candidate in candidates:
        overrideProblem = decoder.get_override_simul_problem(candidate, simulProblem)

        fitInd = -1.0
        try:
            res = simulProblem.simulate(overrideProblem)
            if res.get_solver_status() == solverStatus.OPTIMAL or res.get_solver_status() == solverStatus.SUBOPTIMAL:
                fitInd = config.get_evaluation_function().get_fitness(res, candidate)
                if math.isnan(fitInd):
                    fitInd = -1.0
        except Exception as error:
            print ("Oops! Solver problems.  ", error)
            logging.getLogger('optimModels').warning( "Oops! Solver problems." + str(error))
        fitness.append(fitInd)
    return fitness


# change the original function to start a non-demoniac workers
def parallel_evaluation_mp(candidates, args):
    """
    Evaluate the candidates in parallel using ``multiprocessing``.

    This function allows parallel evaluation of candidate solutions.
    It uses the standard multiprocessing library to accomplish the
    parallelization. The function assigns the evaluation of each
    candidate to its own job, all of which are then distributed to the
    available processing units.

    Args:
        candidates: list the candidate solutions
        args: a dictionary of keyword arguments

    Returns:

    Notes:
    All arguments to the evaluation function must be pickleable.
    Those that are not will not be sent through the ``args`` variable and will be unavailable to your function.
    Required keyword arguments in args:
    - *mp_evaluator* -- actual evaluation function to be used (This function
      should have the same signature as any other inspyred evaluation function.)

    Optional keyword arguments in args:

    - *mp_nprocs* -- number of processors that will be used (default machine
      cpu count)
    """
    logger = logging.getLogger('optimModels')

    try:
        evaluator = args['mp_evaluator']
    except KeyError:
        logger.error('parallel_evaluation_mp requires \'mp_evaluator\' be defined in the keyword arguments list.')
        raise
    try:
        nprocs = args['mp_nprocs']
    except KeyError:
        logger.error('parallel_evaluation_mp requires \'mp_nprocs\' be defined in the keyword arguments list.')
        raise

    pickled_args = {}
    for key in args:
        try:
            pickle.dumps(args[key])
            pickled_args[key] = args[key]
        except (TypeError, pickle.PickleError, pickle.PicklingError):
            logger.debug('unable to pickle args parameter {0} in parallel_evaluation_mp'.format(key))
            pass

    start = time.time()
    try:
        pool = MyPool(processes=nprocs)
        results = [pool.apply_async(evaluator, ([c], pickled_args)) for c in candidates]
        pool.close()
        pool.join()
        return [r.get()[0] for r in results]
    except (OSError, RuntimeError) as e:
        logger.error('failed parallel_evaluation_mp: {0}'.format(str(e)))
        raise
    else:
        end = time.time()
        print('completed parallel_evaluation_mp in {0} seconds'.format(end - start))
        logger.debug('completed parallel_evaluation_mp in {0} seconds'.format(end - start))



