# -*- coding: utf-8 -*-

import sys
from os.path import dirname, join

sys.path.insert(0, join(dirname(__file__), "src"))

from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver
from optimModels.model.dynamicModel import load_kinetic_model

#SBML_MODEL = '../Models/E_coli_Millard2016v2.xml'
SBML_MODEL = '../Models/chassagnole2002.xml'
RESULT_DIR = '../SimulationResults/'

DIL = 0.1/3600
#DIL = 0.1


if __name__ == '__main__':
    model = load_kinetic_model(SBML_MODEL)
    problem = kineticSimulationProblem(model, parameters=None, tSteps = [0,1000], timeout=None)
    print "------------------  ORIGINAL  ------------------"
    #res = problem.simulate(odeSolver.AdamsBashMoulton2)
    #res = problem.simulate(odeSolver.LSODA)
    res = problem.simulate(odeSolver.LSODA)
    print model.metabolites.keys()

    print res.get_fluxes_distribution()
    print "------------------"
    #
    # print "------------------ KO PGI ------------------"
    # overrideProblem = overrideKineticSimProblem(factors = OrderedDict([("vPGI",0.0)]))
    # res = problem.simulate(odeSolver.LSODA, overrideProblem)
    # print res.get_fluxes_distribution()
    # print "------------------"
    #
    # print "------------------ under vPTS ------------------"
    # overrideProblem = overrideKineticSimProblem(factors=OrderedDict([("vPTS", 0.005)]))
    # res = problem.simulate(odeSolver.LSODA,overrideProblem)
    # print res.get_fluxes_distribution()
    # print "------------------"
    #
    # print "------------------ over vPTS ------------------"
    # overrideProblem = overrideKineticSimProblem(factors=OrderedDict([("vPTS", 20)]))
    # res = problem.simulate(odeSolver.LSODA,overrideProblem)
    # print res.get_fluxes_distribution()
    # print "------------------"
