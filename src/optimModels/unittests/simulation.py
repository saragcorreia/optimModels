#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/E_coli_Millard2016v2.xml'
SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed_underoverTest.xml'
#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed_koTest.xml'
#SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
#SBML_MODEL = '/Users/sara/Downloads/Millard2016v2_testing.xml'
RESULT_DIR = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/'

#DIL = 0.1/3600
#DIL = 0.1

from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver

from optimModels.model.dynamicModel import load_kinetic_model
from optimModels.simulation.overrideSimulationProblem import overrideKineticSimProblem
from collections import OrderedDict

if __name__ == '__main__':
    mapParamReacs = {"vE_6PGDH": ["v6PGDH_max"], "vE_Ack": ["vAck_max"], "vE_Ack_medium": ["vAck_max"],
                     "vE_Cya": ["vCya_max"], "vE_Eda": ["vEda_max"], "vE_Edd": ["vEdd_max"], "vE_Fum": ["Fum"],
                     "vE_G6PDH": ["vG6PDH_max"], "vE_MDH": ["MDH"], "vE_Pgi": ["vPgi_max"],
                     "vE_Pgl": ["vPgl_max"], "vE_Pta": ["vPta_max"], "vE_R5PI": ["vR5PI_max"], "vE_Ru5P": ["vRu5P_max"],
                     "vE_Tal": ["vTal_max"], "vE_TktA": ["vTktA_max"], "vE_TktB": ["vTktB_max"],
                     "vE_cAMPdegr": ["vcAMPdegr_max"], "vNonPTS": ["vNonPTS_max"], "vNonPTS_medium": ["vNonPTS_max"],
                     "vPTS4": ["vPTS4_max"], "vPTS4_medium": ["vPTS4_max"], "vE_AceKki": ["AceK"],
                     "vE_AceKph": ["AceK"], "vE_Acs": ["Acs"], "vE_Acs_medium": ["Acs"], "vE_CS": ["CS"],
                     "vE_Fba": ["Fba"], "vE_Fbp": ["Fbp"], "vE_GAPDH": ["GAPDH"], "vE_Glk": ["Glk"],
                     "vE_ICDH": ["ICDH"], "vE_Icl": ["Icl"], "vE_MS": ["MS"], "vE_Mez": ["Mez"], "vE_PDH": ["PDH"],
                     "vE_Pck": ["Pck"], "vE_Pfk": ["Pfk"], "vE_Ppc": ["Ppc"], "vE_Pps": ["Pps"], "vE_Pyk": ["Pyk"],
                     "vE_SDH": ["SDH"], "vE_aKGDH": ["aKGDH"]}

    model = load_kinetic_model(SBML_MODEL, mapParamReacs)
    #model = load_kinetic_model(SBML_MODEL)
    print model.metabolites.keys()

    problem = kineticSimulationProblem(model, tSteps = [0,1e9], timeout=None)
    #print "------------------  ORIGINAL  ------------------"
    #res = problem.simulate(odeSolver.AdamsBashMoulton2)
    #res = problem.simulate(odeSolver.LSODA)
    #res = problem.simulate(odeSolver.LSODA)
    #print model.metabolites.keys()

   # print res.get_fluxes_distribution()
    print "-----------Test under over jahan with parameters -------"
    # test a specific under/over
    #OrderedDict([('vFum1_max', 0), ('vPTS4_max', 32), ('vCya_max', 16), ('Pps', 32)])
    #OrderedDict([('vEdd_max', 0.03125), ('vCya_max', 8), ('Fbp', 0.5), ('Pps', 16), ('Pyk', 0.25), ('vAck_max', 0), ('MDH', 0.03125), ('vPTS4_max', 32)])  15762.88


    #problem = kineticSimulationProblem(model, factors=OrderedDict([('Icl', 16), ('Pps', 32), ('vPTS4_max', 8), ('vG6PDH_max', 0.0625), ('SDH', 0.125)]), tSteps=[0, 1e9])
    #problem = kineticSimulationProblem(model, factors=OrderedDict([('vAck_max', 0),('vcAMPdegr_max', 0),('ICDH', 0)]), tSteps=[0, 1e9])

    problem = kineticSimulationProblem(model, factors=OrderedDict([('v6PGDH_max', 0.03125), ('vAck_max', 0), ('SDH', 0.0625), ('ICDH', 0), ('vPTS4_max', 32)]), tSteps=[0, 1e9])

    #problem = kineticSimulationProblem(model, factors=OrderedDict([('Pps', 32), ('vPTS4_max', 2)]), tSteps=[0, 1e9])

    res = problem.simulate(odeSolver.LSODA)
    print res.get_fluxes_distribution()
    print "------------------"

    print "-----------Test KO jahan -------"
    # test a specific KO
    #'vE_SDH', 'vE_Ack', 'vE_Pyk', 'vE_G6PDH'] --> vSDH1_max = 0, vSDH2_max=0, vAck_max=0, [Pyk] = 0, vG6PDH_max=0
    # problem = kineticSimulationProblem(model, parameters=OrderedDict([('vAck_max',0.0),('vG6PDH_max',0.0),('kSDH1_cat',0),('kSDH2_cat',0),('kPyk_cat',0)]), tSteps=[0, 1e9])
    # res = problem.simulate(odeSolver.LSODA)
    # print res.get_fluxes_distribution()

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