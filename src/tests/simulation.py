SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
RESULT_DIR = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/'

DIL = 0.1/3600
#DIL = 0.1

from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver

from src.optimModels.model.dynamicModel import load_kinetic_model

if __name__ == '__main__':
    model = load_kinetic_model(SBML_MODEL)
    problem = kineticSimulationProblem(model, parameters={'Dil': DIL}, tSteps = [0, 1e9])

    print "------------------  ORIGINAL  ------------------"
    res = problem.simulate(odeSolver.LSODA)
    print res.get_fluxes_distribution()
    print "------------------"

    print "------------------ KO PGI ------------------"
    problem.set_reactions_ko(["vPGI"])
    problem.update_obj()
    res = problem.simulate(odeSolver.LSODA)
    print res.get_fluxes_distribution()
    print "------------------"

    print "------------------ under vPTS ------------------"
    problem.reset_parameters()
    problem.set_factors({"vPTS":0.005})
    problem.update_obj()
    res = problem.simulate(odeSolver.LSODA)
    print res.get_fluxes_distribution()
    print "------------------"

    print "------------------ over vPTS ------------------"
    problem.reset_parameters()
    problem.set_factors({"vPTS": 20})
    problem.update_obj()
    res = problem.simulate(odeSolver.LSODA)
    print res.get_fluxes_distribution()
    print "------------------"