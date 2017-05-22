from optimModels.simulation.simulationProblems import kineticSimulationProblem
from optimModels.utils.simplification import simplify_solutions

from optimModels.model.dynamicModel import load_kinetic_model

KINETIC_MODEL = '../../../examples/models/chassagnole.xml'



if __name__ == '__main__':
    dirResults = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/setEnzReactions/"
    sizes=[6]

    #sbmlFile =  '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    sbmlFile = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/Jahan2016_chemostat_fixed.xml'

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

    model = load_kinetic_model(KINETIC_MODEL, mapParamReacs)
    dils = [(0.1)]
    #dils = [(0.1/3600)]

    problem = kineticSimulationProblem(model, parameters={'Dil': dils[0]}, tSteps=[0, 1e9], timeout=100)

    for size in sizes:
        fileRes = dirResults + 'optim_Jahan_underover_SUC_size' + str(size) + '_True.csv'
        fileFinalRes = dirResults + 'Final_optim_Jahan_underover_SUC_size' + str(size) + '_True.csv'
        #simplify_solutions(problem, fileRes, fileFinalRes, "vsersynth")
        simplify_solutions(problem, fileRes, fileFinalRes, "vD_SUC")
