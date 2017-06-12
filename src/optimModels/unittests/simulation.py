SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
RESULT_DIR = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/'



from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.model.dynamicModel import load_kinetic_model
from optimModels.simulation.overrideSimulationProblem import overrideKineticSimulProblem


def basic_simulation():
    model = load_kinetic_model(SBML_MODEL)
    problem = kineticSimulationProblem(model, tSteps = [0,1e9], timeout=None)
    override = overrideKineticSimulProblem(factors = {'vPTS_rmaxPTS':0, 'vTKA_rmaxTKa':0})
    res = problem.simulate(override)
    res.print_result()


if __name__ == '__main__':
    basic_simulation()

