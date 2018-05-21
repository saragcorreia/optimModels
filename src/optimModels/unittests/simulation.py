from optimModels.model.kineticModel import load_kinetic_model
from framed.cobra.simulation import FBA, pFBA
from framed.io.sbml import load_cbmodel
from optimModels.simulation.simul_problems import StoicSimulationProblem, KineticSimulationProblem
from optimModels.simulation.run import kinetic_simulation
from optimModels.utils.utils import fix_exchange_reactions_model


def medium_test():
    SBML_FILE = "C:/Users/sara/UMinho/Projects/DeCaF/Optimizations/Data/EC_SC_model.xml"
    model = load_cbmodel(SBML_FILE,

                         )
    model2 = fix_exchange_reactions_model(model)

    for r_id, rxn in model2.reactions.items():
        if r_id.startswith('R_EX_'):  # ou tambem podes fazer if rxn.is_exchange:
            rxn.lb = 0
            rxn.ub = 1000 \
                #if rxn.ub is None else rxn.ub


    #sol 1
    constraints = {
    'R_EX_mn2_e__mod1':(-1000,0), 'R_EX_cobalt2_e__mod1':(-1000,0), 'R_EX_cl_e__mod1':(-1000,0), 'R_EX_xyl_D_medium_':(-12,0),
    'R_EX_mobd_e__mod1':(-1000,0), 'R_EX_mg2_e__mod1':(-1000,0),
    'R_EX_o2_medium_':(-2,0), 'R_EX_k_medium_':(-1000,0),
    'R_EX_nh4_medium_':(-1000,0), 'R_EX_fe3_e__mod1':(-1000,0),
    'R_EX_zn2_e__mod1':(-1000,0), 'R_EX_ca2_e__mod1':(-1000,0), 'R_EX_so4_medium_':(-1000,0), 'R_EX_pi_medium_':(-1000,0),
    'R_EX_cu2_e__mod1':(-1000,0)}

    #sol2
    constraints = {
    'R_EX_mn2_e__mod1':(-1000,0), 'R_EX_cobalt2_e__mod1':(-1000,0), 'R_EX_cl_e__mod1':(-1000,0), 'R_EX_mobd_e__mod1':(-1000,0), 'R_EX_cu_e__mod1':(-1000,0),
    'R_EX_mg2_e__mod1':(-1000,0), 'R_EX_glc_D_medium_':(-12,0), 'R_EX_o2_medium_':(-2,0), 'R_EX_k_medium_':(-1000,0), 'R_EX_nh4_medium_':(-1000,0),
    'R_EX_fe3_e__mod1':(-1000,0), 'R_EX_zn2_e__mod1':(-1000,0), 'R_EX_ca2_e__mod1':(-1000,0), 'R_EX_so4_medium_':(-1000,0), 'R_EX_pi_medium_':(-1000,0)}

    res  = pFBA(model2, objective={"R_BM_total_Synth": 1}, constraints=constraints)

    #res  = FBA(model2, objective={"R_BM_total_Synth": 1})

    for r, f in res.values.items():

        print (r + " --> " +str(f))

    print(res.values["R_EX_succ_medium_"])
    print(res.values["R_BM_total_Synth"])
    print(res.values["R_EX_glc_D_medium_"])

def cbm_simualtion_iAF():
    SBML_FILE = "../../../examples/models/Ec_iAF1260.xml"
    model = load_cbmodel(SBML_FILE, flavor="cobra")
    constraints = {'R_Ec_biomass_iAF1260_core_59p81M': (0.55, 9999)}

    res  = FBA(model, objective={"R_EX_succ_e": 1}, constraints=constraints)

    for r, f in res.values.items():
        if f !=0:
            print (r + " --> " +str(f))

    print(res.values["R_EX_succ_e"])
    print(res.values["R_Ec_biomass_iAF1260_core_59p81M"])


def kinetic_sim():
    SBML_FILE = '../../../examples/models/Jahan2016_chemostat_fixed.xml'
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

    model = load_kinetic_model(SBML_FILE, mapParamReacs)
    factors = None
    factors = {'CS': 32, 'v6PGDH_max': 0.0625, 'vEdd_max': 8, 'ICDH': 0.125, 'MS': 8, 'vPta_max': 0, 'SDH': 0.03125, 'vPTS4_max': 32}
    factors = {'ICDH': 0.03125, 'vAck_max': 0, 'SDH': 0.0625, 'vPTS4_max': 32}
    res = kinetic_simulation(model, parameters = None, factors = factors, time = 1e9)

    for r, f in res.get_fluxes_distribution().items():
        print (r + " --> " +str(f))

    for m, c in res.get_steady_state_concentrations().items():
        print(m + " --> " + str(c))

def cbm_simualtion():
    SBML_FILE = "../../../examples/models/iMM904.xml"
    model = load_cbmodel(SBML_FILE, flavor="fbc2")


    constraints = {'R_EX_so4_e': (-10000,0), 'R_EX_o2_e': (-50,0), 'R_EX_gam6p_e': (-10,0), 'R_EX_melib_e': (-5,0)}
    constraints.update({"R_BIOMASS_SC5_notrace":(0.21,9999)})
    res  = FBA(model, objective={"R_EX_etoh_e": 1}, constraints=constraints)
    print(res.values["R_EX_etoh_e"])
    print(res.values["R_BIOMASS_SC5_notrace"])
    print(res.values["R_EX_so4_e"])
    print(res.values["R_EX_gam6p_e"])
    print(res.values["R_EX_o2_e"])
    print(res.values["R_EX_melib_e"])


if __name__ == '__main__':


    kinetic_sim()
