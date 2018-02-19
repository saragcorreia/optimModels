from optimModels.optimization.evaluation_functions import build_evaluation_function
from optimModels.optimization.run import kinetic_strain_optim
from optimModels.model.kineticModel import load_kinetic_model
from optimModels.simulation.simul_problems import KineticSimulationProblem
from optimModels.utils.configurations import KineticConfigurations
from optimModels.utils.configurations import EAConfigurations
from collections import OrderedDict

LEVELS = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
#basePath = "/home/scorreia/Decaf/"
basePath = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/"

def ko_chassagnole():
    sbmlFile = '../../../examples/models/chassagnole2002.xml'
    fileRes = basePath + "Results/optim_Chassagnole_Serine_ko.csv"


    model = load_kinetic_model(sbmlFile)

    objFunc = build_evaluation_function("targetFlux", ["vsersynth"])
    simulProblem = KineticSimulationProblem(model, tSteps=[0, KineticConfigurations.STEADY_STATE_TIME])
    result = kinetic_strain_optim(simulProblem, objFunc=objFunc, levels=None, isMultiProc=False, resultFile=fileRes)
    result.print()


def under_over_chassagnole():
    sbmlFile = '../../../examples/models/chassagnole2002.xml'
    fileRes = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/optim_Chassagnole_Serine_underover.csv"

    model = load_kinetic_model(sbmlFile)

    objFunc = build_evaluation_function("targetFlux", ["vsersynth"])
    simulProblem = KineticSimulationProblem(model, tSteps=[0, KineticConfigurations.STEADY_STATE_TIME])
    result = kinetic_strain_optim(simulProblem, objFunc=objFunc, levels=LEVELS, criticalParameters=[], isMultiProc=False, resultFile=fileRes)
    result.print()


def ko_jahan():
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'
    fileRes = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/optim_Jahan_Suc_ko.csv"
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

    objFunc = build_evaluation_function("targetFlux", ["vD_SUC"])
    simulProblem= KineticSimulationProblem(model, tSteps=[0, KineticConfigurations.STEADY_STATE_TIME])
    result = kinetic_strain_optim(simulProblem, objFunc=objFunc, levels=LEVELS, isMultiProc=False, resultFile=fileRes)
    result.print()

def ko_millard(isMultiProc=False, size=1):
    EAConfigurations.MAX_CANDIDATE_SIZE = size;

    sbmlFile = '../../../examples/models/Millard2016v2.xml'
    fileRes = basePath  + "Results/optim_Millard_acet_ko_"+str(size)+".csv"
    fileLastGen = basePath + "Results/optim_Millard_acet_ko_" + str(size) + "_lastgen.csv"

    mapParamReacs = OrderedDict([('PTS_4', ['eiicbP']), ('PTS_0', ['ei']), ('PTS_1', ['eiP']), ('PTS_2', ['eiia']), ('PTS_3', ['eiicb']),
                      ('PGI', ['PGI_Vmax']), ('PFK', ['PFK_Vmax']), ('FBA', ['FBA_Vmax']), ('TPI', ['TPI_Vmax']),
                      ('GDH', ['GDH_Vmax']), ('PGK', ['PGK_Vmax']), ('GPM', ['GPM_Vmax']), ('ENO', ['ENO_Vmax']),
                      ('PYK', ['PYK_Vmax']), ('ZWF', ['ZWF_Vmax']), ('PGL', ['PGL_Vmax']), ('GND', ['GND_Vmax']),
                      ('RPE', ['RPE_Vmax']), ('RPI', ['RPI_Vmax']), ('X5P_GAP_TKT', ['tkt']), ('F6P_E4P_TKT', ['tktC2']),
                      ('S7P_R5P_TKT', ['tktC2']), ('F6P_GAP_TAL', ['talC3']), ('S7P_E4P_TAL', ['tal']), ('FBP', ['FBP_Vmax']),
                      ('PPC', ['PPC_Vmax']), ('PCK', ['PCK_Vmax']), ('PPS', ['PPS_Vmax']), ('MAD', ['MAD_Vmax']),
                      ('PDH', ['PDH_Vmax']), ('GLT', ['GLT_Vmax']), ('ACN_1', ['ACN_1_Vmax']), ('ACN_2', ['ACN_2_Vmax']),
                      ('ICD', ['icd']), ('LPD', ['LPD_Vmax']), ('SK', ['SK_Vmax']), ('SDH', ['SDH_Vmax']), ('FUMA', ['FUMA_Vmax']),
                      ('MQO', ['MQO_Vmax']), ('MDH', ['MDH_Vmax']), ('ACEA', ['ACEA_Vmax']), ('ACEB', ['ACEB_Vmax']),
                      ('EDD', ['EDD_Vmax']), ('EDA', ['EDA_Vmax']), ('NADH_req', ['NADH_req_Vmax']), ('ATP_syn', ['ATP_syn_Vmax']),
                      ('ACK', ['ACK_Vmax']), ('ACS', ['ACS_Vmax']), ('PTA', ['PTA_Vmax']), ('MYTBO', ['MYTBO_Vmax']),
                      ('SQR', ['SQR_Vmax']), ('NDHII', ['NDHII_Vmax']), ('GROWTH', ['GROWTH_Vmax']), ('ATP_MAINTENANCE', ['ATP_MAINTENANCE_Vmax']),
                      ('XCH_GLC', ['XCH_GLC_Vmax']), ('PIT', ['PIT_Vmax']), ('XCH_P', ['XCH_P_Vmax']), ('XCH_ACE1', ['XCH_ACE1_Vmax']),
                      ('XCH_ACE2', ['XCH_ACE2_Vmax'])])

    model = load_kinetic_model(sbmlFile, mapParamReacs)

    objFunc = build_evaluation_function("targetFlux", ["_ACE_OUT"])
    simulProblem= KineticSimulationProblem(model, tSteps=[0, KineticConfigurations.STEADY_STATE_TIME])

    result = kinetic_strain_optim(simulProblem, objFunc=objFunc, levels=None, criticalParameters=['ATP_MAINTENANCE_Vmax', 'GROWTH_Vmax', 'NDHII_Vmax', 'PIT_Vmax', 'eiicbP', 'ei', 'eiP', 'eiia'], isMultiProc=isMultiProc, resultFile=fileRes, initPopFile=fileLastGen)
    result.print()


def under_over_millard(isMultiProc=False, size=1):
    EAConfigurations.MAX_CANDIDATE_SIZE = size;

    sbmlFile = '../../../examples/models/Millard2016v2.xml'
    fileRes = basePath + "Results/optim_Millard_acet_underover_"+str(size)+".csv"
    fileLastGen = basePath + "Results/optim_Millard_acet_underover_" + str(size) + "_lastgen.csv"
    mapParamReacs = OrderedDict([('PTS_4', ['eiicbP']), ('PTS_0', ['ei']), ('PTS_1', ['eiP']), ('PTS_2', ['eiia']), ('PTS_3', ['eiicb']),
                      ('PGI', ['PGI_Vmax']), ('PFK', ['PFK_Vmax']), ('FBA', ['FBA_Vmax']), ('TPI', ['TPI_Vmax']),
                      ('GDH', ['GDH_Vmax']), ('PGK', ['PGK_Vmax']), ('GPM', ['GPM_Vmax']), ('ENO', ['ENO_Vmax']),
                      ('PYK', ['PYK_Vmax']), ('ZWF', ['ZWF_Vmax']), ('PGL', ['PGL_Vmax']), ('GND', ['GND_Vmax']),
                      ('RPE', ['RPE_Vmax']), ('RPI', ['RPI_Vmax']), ('X5P_GAP_TKT', ['tkt']), ('F6P_E4P_TKT', ['tktC2']),
                      ('S7P_R5P_TKT', ['tktC2']), ('F6P_GAP_TAL', ['talC3']), ('S7P_E4P_TAL', ['tal']), ('FBP', ['FBP_Vmax']),
                      ('PPC', ['PPC_Vmax']), ('PCK', ['PCK_Vmax']), ('PPS', ['PPS_Vmax']), ('MAD', ['MAD_Vmax']),
                      ('PDH', ['PDH_Vmax']), ('GLT', ['GLT_Vmax']), ('ACN_1', ['ACN_1_Vmax']), ('ACN_2', ['ACN_2_Vmax']),
                      ('ICD', ['icd']), ('LPD', ['LPD_Vmax']), ('SK', ['SK_Vmax']), ('SDH', ['SDH_Vmax']), ('FUMA', ['FUMA_Vmax']),
                      ('MQO', ['MQO_Vmax']), ('MDH', ['MDH_Vmax']), ('ACEA', ['ACEA_Vmax']), ('ACEB', ['ACEB_Vmax']),
                      ('EDD', ['EDD_Vmax']), ('EDA', ['EDA_Vmax']), ('NADH_req', ['NADH_req_Vmax']), ('ATP_syn', ['ATP_syn_Vmax']),
                      ('ACK', ['ACK_Vmax']), ('ACS', ['ACS_Vmax']), ('PTA', ['PTA_Vmax']), ('MYTBO', ['MYTBO_Vmax']),
                      ('SQR', ['SQR_Vmax']), ('NDHII', ['NDHII_Vmax']), ('GROWTH', ['GROWTH_Vmax']), ('ATP_MAINTENANCE', ['ATP_MAINTENANCE_Vmax']),
                      ('XCH_GLC', ['XCH_GLC_Vmax']), ('PIT', ['PIT_Vmax']), ('XCH_P', ['XCH_P_Vmax']), ('XCH_ACE1', ['XCH_ACE1_Vmax']),
                      ('XCH_ACE2', ['XCH_ACE2_Vmax'])])

    model = load_kinetic_model(sbmlFile, mapParamReacs)

    objFunc = build_evaluation_function("targetFlux", ["_ACE_OUT"])
    simulProblem= KineticSimulationProblem(model, tSteps=[0, KineticConfigurations.STEADY_STATE_TIME])
    result = kinetic_strain_optim(simulProblem, objFunc=objFunc, levels=LEVELS, criticalParameters=['ATP_MAINTENANCE_Vmax', 'GROWTH_Vmax', 'NDHII_Vmax', 'PIT_Vmax', 'eiicbP', 'ei', 'eiP', 'eiia'], isMultiProc=isMultiProc, resultFile=fileRes, initPopFile=fileLastGen)
    result.print()


if __name__ == '__main__':
    import time
    import warnings
    import sys
    size = 1

    warnings.filterwarnings('ignore')  # ignore the warnings related to floating points raise from solver!!!
    t1 = time.time()
    #ko_millard(True,size)
    under_over_millard(True, size)
    t2 = time.time()
    print ("time with multiproccessing" + str(t2 - t1))

