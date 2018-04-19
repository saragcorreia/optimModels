from optimModels.optimization.decoders import DecoderReacKnockouts, DecoderReacUnderOverExpression
import itertools
from optimModels.optimization.run import load_population
from optimModels.model.kineticModel import load_kinetic_model
from collections import OrderedDict
from optimModels.simulation.override_simul_problem import OverrideKineticSimulProblem
from optimModels.optimization.evaluation_functions import build_evaluation_function
from optimModels.simulation.simul_problems import KineticSimulationProblem
from optimModels.utils.configurations import KineticConfigurations


def jahan_model():
    sbmlFile = '../../../examples/models/Jahan2016_chemostat_fixed.xml'
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
    simulProblem = KineticSimulationProblem(model, tSteps=[0, KineticConfigurations.STEADY_STATE_TIME], timeout=60)
    idsToManipulate = list(set(itertools.chain.from_iterable(simulProblem.model.reacParamsFactors.values())))

    return simulProblem, idsToManipulate


def millard_model():
    sbmlFile = '../../../examples/models/Millard2016_suc_drain.xml'
    mapParamReacs = {'PTS_4': ['eiicbP'], 'PTS_0': ['ei'], 'PTS_1': ['eiP'], 'PTS_2': ['eiia'], 'PTS_3': ['eiicb'],
         'PGI': ['PGI_Vmax'], 'PFK': ['PFK_Vmax'], 'FBA': ['FBA_Vmax'], 'TPI': ['TPI_Vmax'],
         'GDH': ['GDH_Vmax'], 'PGK': ['PGK_Vmax'], 'GPM': ['GPM_Vmax'], 'ENO': ['ENO_Vmax'],
         'PYK': ['PYK_Vmax'], 'ZWF': ['ZWF_Vmax'], 'PGL': ['PGL_Vmax'], 'GND': ['GND_Vmax'],
         'RPE': ['RPE_Vmax'], 'RPI': ['RPI_Vmax'], 'X5P_GAP_TKT': ['tkt'], 'F6P_E4P_TKT': ['tktC2'],
         'S7P_R5P_TKT': ['tktC2'], 'F6P_GAP_TAL': ['talC3'], 'S7P_E4P_TAL': ['tal'], 'FBP': ['FBP_Vmax'],
         'PPC': ['PPC_Vmax'], 'PCK': ['PCK_Vmax'], 'PPS': ['PPS_Vmax'], 'MAD': ['MAD_Vmax'],
         'PDH': ['PDH_Vmax'], 'GLT': ['GLT_Vmax'], 'ACN_1': ['ACN_1_Vmax'], 'ACN_2': ['ACN_2_Vmax'],
         'ICD': ['icd'], 'LPD': ['LPD_Vmax'], 'SK': ['SK_Vmax'], 'SDH': ['SDH_Vmax'], 'FUMA': ['FUMA_Vmax'],
         'MQO': ['MQO_Vmax'], 'MDH': ['MDH_Vmax'], 'ACEA': ['ACEA_Vmax'], 'ACEB': ['ACEB_Vmax'],
         'EDD': ['EDD_Vmax'], 'EDA': ['EDA_Vmax'], 'NADH_req': ['NADH_req_Vmax'], 'ATP_syn': ['ATP_syn_Vmax'],
         'ACK': ['ACK_Vmax'], 'ACS': ['ACS_Vmax'], 'PTA': ['PTA_Vmax'], 'MYTBO': ['MYTBO_Vmax'],
         'SQR': ['SQR_Vmax'], 'NDHII': ['NDHII_Vmax'], 'GROWTH': ['GROWTH_Vmax'],
         'ATP_MAINTENANCE': ['ATP_MAINTENANCE_Vmax'],
         'XCH_GLC': ['XCH_GLC_Vmax'], 'PIT': ['PIT_Vmax'], 'XCH_P': ['XCH_P_Vmax'],
         'XCH_ACE1': ['XCH_ACE1_Vmax'],
         'XCH_ACE2': ['XCH_ACE2_Vmax']}

    model = load_kinetic_model(sbmlFile, mapParamReacs)
    simulProblem = KineticSimulationProblem(model, tSteps=[0, KineticConfigurations.STEADY_STATE_TIME], timeout=600)
    critParams = ['ATP_MAINTENANCE_Vmax', 'GROWTH_Vmax', 'NDHII_Vmax', 'PIT_Vmax', 'eiicbP', 'ei', 'eiP', 'eiia']
    allParams = list(set(itertools.chain.from_iterable(simulProblem.model.reacParamsFactors.values())))
    idsToManipulate = [x for x in allParams if x not in critParams]

    return simulProblem, idsToManipulate


def simplify_solution(simulProblem, decoder, evalFunc, solutions):
    result=[]
    for sol in solutions:
        ind = decoder.decode_candidate_ids_to_index(sol)
        override = decoder.get_override_simul_problem(ind, simulProblem)
        res = simulProblem.simulate(override)
        # fitness of solution
        fitness = evalFunc.get_fitness(res, override.factors)

        # do not simplify solutions with fitness == 0 and with a single modification
        if float(fitness) > 0.0 and len(override.get_modifications()) > 1:
            factorsOrig = override.factors.copy()
            print("simplify")
            for k, v in factorsOrig.items():
                del override.factors[k]

                try:
                    res = simulProblem.simulate(override)
                    newFitness = evalFunc.get_fitness(res, override.factors)
                except Exception:
                    newFitness = -1.0
                print(fitness, " ---- ", k, "----", newFitness)
                if round(fitness, 12) != round(newFitness, 12):
                    override.factors[k] = v



        print(override.get_modifications())
        result.append(simulProblem.simulate(override))
    return result

def simulate_solutions(simulProblem, decoder, solutions):
    result=[]
    if len(solutions)==0:
        result.append(simulProblem.simulate())
    for sol in solutions:
        ind = decoder.decode_candidate_ids_to_index(sol)
        override = decoder.get_override_simul_problem(ind, simulProblem)
        result.append(simulProblem.simulate(override))
    return result

def yield_solutions(simulationResults, productId, uptakeId):

    for res in simulationResults:
        #for k, v in res.ssFluxesDistrib.items():
        #    print( k ,": ",v)
        #print ("-----conc-----")
        #for k, v in res.ssConcentrations.items():
        #    print(k, ": ", v)

        if res.get_override_simul_problem():
            print ("----- Yield ------" + str(res.get_override_simul_problem().factors))
        if len(res.ssFluxesDistrib)>0:
            print ("yield: "+ str(res.ssFluxesDistrib[productId] / res.ssFluxesDistrib[uptakeId]))
            print("uptake: "+ str(res.ssFluxesDistrib[uptakeId]))
            print("product: "+ str(res.ssFluxesDistrib[productId]))

def jahan_ko():
    simulProblem, idsToManipulate = jahan_model()
    decoder = DecoderReacKnockouts(idsToManipulate)
    evalFunc = build_evaluation_function("targetFlux", ["vD_SUC"])

    solutions = [['CS', 'Pps', 'MS', 'MDH', 'Pfk', 'vTktB_max', 'vAck_max', 'v6PGDH_max', 'Ppc'],
                ['CS', 'Pps', 'Icl', 'MS', 'MDH', 'Pfk', 'vTktB_max', 'vAck_max', 'v6PGDH_max', 'Ppc'] ,
                ['CS', 'MDH', 'aKGDH', 'vPta_max', 'Ppc'],
                ['CS', 'Pps', 'MS', 'MDH', 'vPta_max', 'Ppc'] ,
                ['CS', 'Pps', 'Icl', 'MS', 'MDH', 'vPta_max', 'Ppc'] ,
                ['CS', 'Pps', 'Icl', 'MS', 'MDH', 'vPta_max', 'Ppc', 'Fbp'] ,
                ['CS', 'MDH', 'vPta_max', 'Ppc', 'Pps'] ,
                ['CS', 'Pps', 'MDH', 'vAck_max', 'v6PGDH_max', 'Ppc'] ,
                ['vPgi_max', 'vPta_max', 'Ppc'] ,
                ['CS', 'MDH', 'vPta_max', 'Ppc'] ,
                ['CS', 'MDH', 'vPta_max', 'Ppc', 'Pps'] ,
                ['vPgi_max', 'vPta_max', 'Ppc'] ,
                ['CS', 'MDH', 'vPta_max', 'Ppc'] ,
                ['vPgi_max', 'vPta_max', 'Ppc'] ,
                ['vAck_max', 'Ppc'] ,
                ['vPTS4_max'] ]
    results = simulate_solutions(simulProblem, decoder, solutions)
    yield_solutions(results, "vD_SUC","vD_GLCfeed" )
    #simplify_solution(simulProblem,  decoder, evalFunc,  solutions)

def jahan_uo():
    simulProblem, idsToManipulate = jahan_model()
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
    decoder = DecoderReacUnderOverExpression(idsToManipulate, levels)
    evalFunc = build_evaluation_function("targetFlux", ["vD_SUC"])
    solutions =[
           # OrderedDict([('CS', 32), ('PDH', 32), ('Fbp', 32), ('MS', 16), ('ICDH', 0), ('vNonPTS_max', 32), ('SDH', 0.03125),('v6PGDH_max', 0), ('vPTS4_max', 32), ('vAck_max', 0)]),
           # OrderedDict([('SDH', 0.0625), ('Pyk', 0), ('vG6PDH_max', 0.03125), ('vPta_max', 0), ('CS', 8), ('Fbp', 4), ('Ppc', 32),('vPTS4_max', 32)]),
           # OrderedDict([('Pyk', 0), ('vG6PDH_max', 0.03125), ('vPta_max', 0), ('Fbp', 4), ('SDH', 0.0625), ('CS', 8),('vPTS4_max', 32), ('Ppc', 32)]),
        #OrderedDict([('vG6PDH_max', 0), ('vPta_max', 0), ('MS', 16), ('ICDH', 0), ('SDH', 0.0625), ('vPTS4_max', 32)]),
        #OrderedDict([('SDH', 0.125), ('vG6PDH_max', 0.03125), ('vPTS4_max', 32), ('ICDH', 0), ('vAck_max', 0)])
        {'Ppc': 4, 'v6PGDH_max': 16, 'Fbp': 4, 'Pps': 16, 'Pyk': 0.03125, 'vPta_max': 0, 'SDH': 0.25, 'vPTS4_max': 16}
        #OrderedDict([('v6PGDH_max', 0.0625), ('SDH', 0.03125), ('vAck_max', 0), ('vPTS4_max', 32), ('ICDH', 0)]),
        #OrderedDict([('v6PGDH_max', 0.0625), ('SDH', 0.03125), ('vAck_max', 0), ('vPTS4_max', 32)]),
        #OrderedDict([('v6PGDH_max', 0.0625), ('SDH', 0.03125), ('vAck_max', 0), ('ICDH', 0)]),
        #OrderedDict([('v6PGDH_max', 0.0625), ('SDH', 0.03125), ('vPTS4_max', 32), ('ICDH', 0)]),
        #OrderedDict([('v6PGDH_max', 0.0625), ('vAck_max', 0), ('vPTS4_max', 32), ('ICDH', 0)]),
        #OrderedDict([ ('SDH', 0.03125), ('vAck_max', 0), ('vPTS4_max', 32), ('ICDH', 0)]),
           # OrderedDict([('ICDH', 0.125), ('vPta_max', 0), ('SDH', 0.25), ('vPTS4_max', 32)]),
            #OrderedDict([('vPta_max', 0), ('ICDH', 0.125), ('SDH', 0.25), ('vPTS4_max', 32)]),
           # OrderedDict([('ICDH', 0.125), ('SDH', 0.03125), ('vAck_max', 0)]),
           # OrderedDict([('SDH', 0.03125), ('Pps', 32)]),
           # OrderedDict([('Pps', 32)])
    ]
    #results = simulate_solutions(simulProblem, decoder, [])
    #yield_solutions(results, "vD_SUC", "vD_GLCfeed")


    print("WITH UO")
    results = simulate_solutions(simulProblem, decoder, solutions)
    yield_solutions(results, "vD_SUC","vD_GLCfeed" )

def millard_ko():
    simulProblem, idsToManipulate = millard_model()
    decoder = DecoderReacKnockouts(idsToManipulate)

    solutions = [
                #['tktC2', 'RPI_Vmax', 'GND_Vmax', 'SDH_Vmax', 'PPS_Vmax', 'PGI_Vmax', 'tkt', 'talC3', 'tal'],
                #['ACEB_Vmax', 'PGI_Vmax', 'GND_Vmax', 'ACS_Vmax', 'tal', 'tktC2', 'RPI_Vmax', 'SDH_Vmax', 'tkt','talC3'],
                ['NADH_req_Vmax', 'RPI_Vmax', 'talC3', 'SDH_Vmax', 'GND_Vmax', 'PCK_Vmax', 'tal'],
                #['PCK_Vmax', 'tal', 'NADH_req_Vmax', 'RPI_Vmax', 'PPS_Vmax', 'GND_Vmax', 'talC3', 'SQR_Vmax'],
                #['GND_Vmax', 'tal', 'EDD_Vmax', 'talC3', 'PTA_Vmax', 'SQR_Vmax'],
                #['tal', 'talC3', 'PGL_Vmax', 'SDH_Vmax'],
                #['PGL_Vmax', 'talC3', 'tal', 'ACK_Vmax', 'SDH_Vmax'],
                #['tal', 'talC3', 'PGL_Vmax', 'SQR_Vmax'],
                #['PGL_Vmax', 'SDH_Vmax'],
                #['ZWF_Vmax', 'SDH_Vmax', 'RPE_Vmax'],
                #['ZWF_Vmax', 'RPE_Vmax', 'SQR_Vmax'],
                #['PGL_Vmax', 'SDH_Vmax'],
                #['FUMA_Vmax']
                ]

    #simplify_solution(simulProblem, decoder, solutions)
    results = simulate_solutions(simulProblem, decoder, solutions)
    yield_solutions(results, "_SUC_OUT","GLC_feed" )

def millard_uo():
    simulProblem, idsToManipulate = millard_model()
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
    decoder = DecoderReacUnderOverExpression(idsToManipulate, levels)

    solutions =[
                #{'EDD_Vmax': 32, 'eiicb': 0.0625, 'GDH_Vmax': 32, 'MAD_Vmax': 0, 'ACN_1_Vmax': 0, 'MQO_Vmax': 32, 'ACN_2_Vmax': 16, 'EDA_Vmax': 0.03125} ,
                #{'EDD_Vmax': 32, 'eiicb': 0.0625, 'GDH_Vmax': 32, 'XCH_ACE1_Vmax': 16, 'MAD_Vmax': 0, 'ACN_1_Vmax': 0, 'MQO_Vmax': 32, 'ACN_2_Vmax': 16, 'EDA_Vmax': 0.03125} ,
                {'LPD_Vmax': 32, 'FUMA_Vmax': 0, 'tktC2': 16, 'tkt': 0, 'GND_Vmax': 4, 'ZWF_Vmax': 16, 'ACK_Vmax': 8} , #OK
                {'LPD_Vmax': 32, 'FUMA_Vmax': 0, 'tktC2': 16, 'GLT_Vmax': 32, 'tkt': 0, 'GND_Vmax': 4, 'ACEA_Vmax': 32, 'ZWF_Vmax': 16} , #OK
                {'FUMA_Vmax': 0, 'tkt': 0, 'LPD_Vmax': 32, 'ZWF_Vmax': 32, 'tktC2': 32} , # OK
                {'LPD_Vmax': 32, 'FUMA_Vmax': 0, 'tktC2': 32, 'tkt': 0, 'ZWF_Vmax': 32, 'ATP_syn_Vmax': 8} , #OK
                {'talC3': 16, 'tal': 0.125, 'SDH_Vmax': 0, 'ZWF_Vmax': 32, 'LPD_Vmax': 32} , #OK
                {'talC3': 32, 'PGI_Vmax': 0.03125, 'SQR_Vmax': 0, 'LPD_Vmax': 32} , #OK
                {'talC3': 32, 'SDH_Vmax': 0, 'PGI_Vmax': 0.03125} ,  #OK
                {'talC3': 32, 'SDH_Vmax': 0} ,
                {'FUMA_Vmax': 0} #OK
         ]

    results = simulate_solutions(simulProblem, decoder, solutions)
    yield_solutions(results, "_SUC_OUT", "XCH_GLC")

if __name__=='__main__':
    print("Jahan knockouts")
    #jahan_ko()
    print("Jahan under over expression")
    jahan_uo()

    print("Millard KO")
    #millard_ko()

    print("Millard under over expression")
    #millard_ko()