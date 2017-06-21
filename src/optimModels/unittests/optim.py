from optimModels.optimization.objectiveFunctions import build_objective_function
from optimModels.optimization.run import strain_optim
from optimModels.model.kineticModel import load_kinetic_model
from optimModels.simulation.simulationResults import print_simul_result

LEVELS = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]


def ko_chassagnole():
    sbmlFile = '../../../examples/models/chassagnole2002.xml'
    fileRes = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/optim_Chassagnole_Serine_ko.csv"


    model = load_kinetic_model(sbmlFile)

    objFunc = build_objective_function("targetFlux", ["vsersynth"])

    result = strain_optim(model, objFunc=objFunc, levels=None, criticalGenes=[], isMultiProc=False, resultFile=fileRes)
    for r in result:
        print print_simul_result(r)


def under_over_chassagnole():
    sbmlFile = '../../../examples/models/chassagnole2002.xml'
    fileRes = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/optim_Chassagnole_Serine_underover.csv"

    model = load_kinetic_model(sbmlFile)

    objFunc = build_objective_function("targetFlux", ["vsersynth"])

    result = strain_optim(model, objFunc=objFunc, levels=LEVELS, criticalGenes=[], isMultiProc=False, resultFile=fileRes)
    for r in result:
        print print_simul_result(r)


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

    objFunc = build_objective_function("targetFlux", ["vD_SUC"])

    result = strain_optim(model, objFunc=objFunc, levels=LEVELS, criticalGenes=[], isMultiProc=False, resultFile=fileRes)
    for r in result:
        print print_simul_result(r)

if __name__ == '__main__':
    import time
    import warnings
    warnings.filterwarnings('ignore')  # ignore the warnings related to floating points raise from solver!!!
    t1 = time.time()
    ko_jahan()
    t2 = time.time()
    print "time with multiproccessing" + str(t2 - t1)

    t1 = time.time()
    under_over_chassagnole()
    t2 = time.time()
    print "time with multiproccessing" + str(t2 - t1)