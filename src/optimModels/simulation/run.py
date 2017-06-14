import copy

from optimModels.model.kineticModel import load_kinetic_model
from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.overrideSimulationProblem import overrideKineticSimulProblem
from optimModels.utils.configurations import EAConfigurations

def steady_state_simulation(model, parameters = None, factors = None, time = 1e9):
    """
    Function to perform the strain optimization using kinetic metabolic models.

    Parameters
    ----------
    model : kineticModel
        The kinetic metabolic model.
    parameters : dict
        List of parameters that will be set with new values (ex: Dilution, initial concentrations).
    factors : dict
        Values to by multiplied to the vMax parameters (KO: the value should be 0, Under: value between 0 and 1,
        Over: value higher than 1)
    time :  float
        End time for steady-state.
    Returns
    -------
    out : kineticSimulationResults
        The function returns the best solutions found in strain optimization. The kineticSimulationResults have the
        flux distribution and metabolites concentration on steady-state, and the modifications made over the
        original model.

    """

    simulProblem = kineticSimulationProblem(model, parameters = parameters , tSteps=[0, time])

    if factors:
        override = overrideKineticSimulProblem(factors = factors)
        result = simulProblem.simulate(override)
    else:
        result = simulProblem.simulate()

    return result