#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/E_coli_Millard2016v2.xml'
#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed_underoverTest.xml'
SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed_koTest.xml'
#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
RESULT_DIR = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/'

#DIL = 0.1/3600
#DIL = 0.1

from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver

from optimModels.model.dynamicModel import load_kinetic_model
from optimModels.simulation.overrideSimulationProblem import overrideKineticSimProblem
from collections import OrderedDict

if __name__ == '__main__':
    model = load_kinetic_model(SBML_MODEL)

    #problem = kineticSimulationProblem(model, parameters=None, tSteps = [0,1e9], timeout=100)
    #print "------------------  ORIGINAL  ------------------"
    #res = problem.simulate(odeSolver.AdamsBashMoulton2)
    #res = problem.simulate(odeSolver.LSODA)
    #res = problem.simulate(odeSolver.LSODA)
    #print model.metabolites.keys()

    #print res.get_fluxes_distribution()
    # print "-----------Test under over jahan with parameters -------"
    # # test a specific under/over
    # #[('vE_Pps', 32), ('vE_Pta', 0), ('vE_Pck', 16)])
    # problem = kineticSimulationProblem(model, parameters=OrderedDict([('vPta_max',0)]), tSteps=[0, 1e9])
    # res = problem.simulate(odeSolver.LSODA)
    # print res.get_fluxes_distribution()
    # print "------------------"

    print "-----------Test KO jahan -------"
    # test a specific KO
    #'vE_SDH', 'vE_Ack', 'vE_Pyk', 'vE_G6PDH'] --> vSDH1_max = 0, vSDH2_max=0, vAck_max=0, [Pyk] = 0, vG6PDH_max=0
    problem = kineticSimulationProblem(model, parameters=OrderedDict([('vAck_max',0.0),('vG6PDH_max',0.0)]), tSteps=[0, 1e9])
    res = problem.simulate(odeSolver.LSODA)
    print res.get_fluxes_distribution()

    # print "-----------Test under over jahan with factors -------"
    # problem = kineticSimulationProblem(model, parameters=None, tSteps=[0, 1e9], timeout=50)
    # overrideProblem = overrideKineticSimProblem(factors = OrderedDict([('vE_Pps',32),('vE_Pta',0),('vE_Pck',16)]))
    # res = problem.simulate(odeSolver.LSODA, overrideProblem)
    # print res.get_fluxes_distribution()


    # # Chassagnole model
    # print "------------------ KO PGI ------------------"
    # overrideProblem = overrideKineticSimProblem(factors = OrderedDict([("PGI",0.0)]))
    # res = problem.simulate(odeSolver.LSODA, overrideProblem)
    # print res.get_fluxes_distribution()
    # print "------------------"
    #
    # print "------------------ under vPTS ------------------"
    # overrideProblem = overrideKineticSimProblem(factors=OrderedDict([("PTS", 0.005)]))
    # res = problem.simulate(odeSolver.LSODA,overrideProblem)
    # print res.get_fluxes_distribution()
    # print "------------------"
    #
    # print "------------------ over vPTS ------------------"
    # overrideProblem = overrideKineticSimProblem(factors=OrderedDict([("PTS", 20)]))
    # res = problem.simulate(odeSolver.LSODA,overrideProblem)
    # print res.get_fluxes_distribution()
    # print "------------------"



    #Jahan model
    # print "------------------ KO vE_Pck ------------------"
    # overrideProblem = overrideKineticSimProblem(factors = OrderedDict([("vE_Pck",0.0)]))
    # res = problem.simulate(odeSolver.LSODA, overrideProblem)
    # print res.get_fluxes_distribution()
    # print "------------------"
    #
    # print "------------------ under vE_Pck ------------------"
    # overrideProblem = overrideKineticSimProblem(factors=OrderedDict([("vE_Pck", 0.005)]))
    # res = problem.simulate(odeSolver.LSODA,overrideProblem)
    # print res.get_fluxes_distribution()
    # print "------------------"
    #
    # print "------------------ over vE_Pck ------------------"
    # overrideProblem = overrideKineticSimProblem(factors=OrderedDict([("vE_Pck", 20)]))
    # res = problem.simulate(odeSolver.LSODA,overrideProblem)
    # print res.get_fluxes_distribution()
    # print "------------------"