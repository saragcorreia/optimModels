from optimModels.optimization.decoders import decoderReactionsKnockouts, decoderUnderOverExpression
from optimModels.optimization.evolutionaryComputation import optimProblemConfiguration, optimization_intSetRep, \
    optimization_tupleSetRep
from optimModels.optimization.objectiveFunctions import targetFlux
from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.simulation.solvers import odeSolver
from optimModels.model.dynamicModel import load_kinetic_model

basePath = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations"
#basePath = ""

def ko_chassagnole(isMultiProc=False):
    sbmlFile = basePath+'/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1 / 3600}, tSteps=[0, 1e9])
    res = problem.simulate(odeSolver.LSODA)
    print "Serine in WT ....."
    print res.get_fluxes_distribution()['vsersynth']

    reactionsToManipulate =['vPTS', 'vPGI', 'vPGM', 'vG6PDH', 'vPFK', 'vTA', 'vTKA', 'vTKB', 'vMURSyNTH', 'vALDO', 'vGAPDH', 'vTIS', 'vTRPSYNTH', 'vG3PDH', 'vPGK', 'vsersynth', 'vrpGluMu', 'vENO', 'vPK', 'vpepCxylase', 'vSynth1', 'vSynth2', 'vDAHPS', 'vPDH', 'vMethSynth', 'vPGDH', 'vR5PI', 'vRu5P', 'vPPK', 'vG1PAT']

    print reactionsToManipulate


    prob = optimProblemConfiguration(problem, decoder=decoderReactionsKnockouts(reactionsToManipulate),
                                     objectiveFunc=targetFlux("vsersynth"),
                                     solverId=odeSolver.LSODA)


    prob.set_optim_parameters(popSize=100, maxGenerations=10, popSelectedSize=50, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [0, len(reactionsToManipulate) - 1]

    optimization_intSetRep(prob, bounds,
                           basePath+"/Results/optim_Chassagnole_Serine_size5" + str(
                               isMultiProc) + ".csv",
                           isMultiProc=isMultiProc)


def underover_chassagnole(isMultiProc):
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
    sbmlFile = basePath+'/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1 / 3600}, tSteps=[0, 1e9])
    res = problem.simulate(odeSolver.LSODA)
    print "Serine in WT ...ko_chassagnole.."
    print res.get_fluxes_distribution()['vsersynth']

    reactionsToManipulate =['vPTS', 'vPGI', 'vPGM', 'vG6PDH', 'vPFK', 'vTA', 'vTKA', 'vTKB', 'vMURSyNTH', 'vALDO', 'vGAPDH', 'vTIS', 'vTRPSYNTH', 'vG3PDH', 'vPGK', 'vsersynth', 'vrpGluMu', 'vENO', 'vPK', 'vpepCxylase', 'vSynth1', 'vSynth2', 'vDAHPS', 'vPDH', 'vMethSynth', 'vPGDH', 'vR5PI', 'vRu5P', 'vPPK', 'vG1PAT']
    prob = optimProblemConfiguration(problem, decoder=decoderUnderOverExpression(reactionsToManipulate,levels),
                                     objectiveFunc=targetFlux("vsersynth"),
                                     solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=100, maxGenerations=10, popSelectedSize=50, maxCandidateSize=5,
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [[0, 0], [len(reactionsToManipulate) - 1, len(levels) - 1]]

    optimization_tupleSetRep(prob, bounds,
                             resultFile="/Volumes/Data/Documents/Projects/DeCaF/Optimizations/ResultsEXP/optim_Chassagnole_Serine_size5" + str(
                                 isMultiProc) + ".csv", isMultiProc=isMultiProc)


    #################
def ko_jahan(isMultiProc=False, size = 1):
    sbmlFile = basePath+'/Data/Jahan2016_chemostat_fixed.xml'
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

    model = load_kinetic_model(sbmlFile, mapParamReacs)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1}, tSteps=[0, 1e9], timeout = 100)
    res = problem.simulate(odeSolver.LSODA)
    print "vD_SUC in WT ....."
    print res.get_fluxes_distribution()['vD_SUC']

    toManipulate = sum(mapParamReacs.values(),[])

    prob = optimProblemConfiguration(problem, decoder=decoderReactionsKnockouts(toManipulate), objectiveFunc=targetFlux("vD_SUC"),
                                     solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=100, maxGenerations=5, popSelectedSize=50, maxCandidateSize=int(size),
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [0, len(toManipulate) - 1]

    final_pop = optimization_intSetRep(prob, bounds,
                                       basePath+"/Results/optim_Jahan_ko_SUCXXXX_size_"+ str(size)+"_" + str(
                                           isMultiProc) + ".csv",
                                       isMultiProc=isMultiProc)


def underover_jahan(isMultiProc=False, size=1):
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
    sbmlFile = basePath+'/Data/Jahan2016_chemostat_fixed.xml'
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

    model = load_kinetic_model(sbmlFile)

    #set associations
    model.set_reactions_parameters_association(mapParamReacs)

    problem = kineticSimulationProblem(model, parameters={'Dil': 0.1}, tSteps=[0, 1e9], timeout = 300)
    res = problem.simulate(odeSolver.LSODA)
    print "vD_SUC in WT ...."
    print res.get_fluxes_distribution()['vD_SUC']

    toManipulate = sum(mapParamReacs.values(), [])


    prob = optimProblemConfiguration(problem, decoder=decoderUnderOverExpression(toManipulate,levels),
                                     objectiveFunc=targetFlux("vD_SUC"),
                                     solverId=odeSolver.LSODA)

    prob.set_optim_parameters(popSize=100, maxGenerations=500, popSelectedSize=50, maxCandidateSize=int(size),
                              crossoverRate=1.0, mutationRate=0.1, newCandidatesRate=0.1)

    # define the max limit for index of reactions and levels
    bounds = [[0, 0], [len(toManipulate) - 1, len(levels) - 1]]

    final_pop = optimization_tupleSetRep(prob, bounds,
                                         resultFile=basePath+"/Results/optim_Jahan_SUC_size_" + str(size)+"_" + str(isMultiProc) + ".csv",
                                         isMultiProc=isMultiProc)

    #################

if __name__ == '__main__':
    import time
    import warnings
    warnings.filterwarnings('ignore')  # ignore the warnings related to floating points raise from solver!!!
    t1 = time.time()
    size = 4
    ko_jahan(True, size)
    t2 = time.time()
    t3 = time.time()
    #underover_chassagnole(True)
    t4 = time.time()
    print "time for 10 generations with multiproccessing" + str(t2 - t1)
    print "time for 10 generations with multiproccessing 904 - " + str(t4 - t3)
    # underover_chassagnole()
