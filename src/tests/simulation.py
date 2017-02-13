SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
RESULT_DIR = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/'

DIL = 0.1/3600
#DIL = 0.1

from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver

from optimModels.model.dynamicModel import load_kinetic_model
from optimModels.simulation.overrideSimulationProblem import overrideKineticSimProblem
from collections import OrderedDict

if __name__ == '__main__':
    model = load_kinetic_model(SBML_MODEL)
    problem = kineticSimulationProblem(model, parameters={'Dil': DIL}, tSteps = [0, 1e9])

    print "------------------  ORIGINAL  ------------------"
    res = problem.simulate(odeSolver.LSODA)
    print res.get_fluxes_distribution()
    print "------------------"

    print "------------------ KO PGI ------------------"
    overrideProblem = overrideKineticSimProblem(factors = OrderedDict([("vPGI",0.0)]))
    res = problem.simulate(odeSolver.LSODA, overrideProblem)
    print res.get_fluxes_distribution()
    print "------------------"

    print "------------------ under vPTS ------------------"
    overrideProblem = overrideKineticSimProblem(factors=OrderedDict([("vPTS", 0.005)]))
    res = problem.simulate(odeSolver.LSODA,overrideProblem)
    print res.get_fluxes_distribution()
    print "------------------"

    print "------------------ over vPTS ------------------"
    overrideProblem = overrideKineticSimProblem(factors=OrderedDict([("vPTS", 20)]))
    res = problem.simulate(odeSolver.LSODA,overrideProblem)
    print res.get_fluxes_distribution()
    print "------------------"