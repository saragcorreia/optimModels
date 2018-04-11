
from optimModels.simulation.run import kinetic_simulation


from optimModels.model.kineticModel import load_kinetic_model
from framed.cobra.simulation import FBA, pFBA
from framed.io.sbml import load_cbmodel
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.utils import fix_exchange_reactions_model

def sophia_test():
    SBML_FILE = "C:/Users/sara/UMinho/Projects/DeCaF/Optimizations/Data/EC_SC.xml"
    model = load_cbmodel(SBML_FILE, exchange_detection_mode="R_EX_")
    model2 = fix_exchange_reactions_model(model)

    constraints = {'R_EX_mn2_e__mod1':(-100,0),'R_EX_xyl_D_e_':(-100, -20), 'R_EX_so4_e_':(-100,0), 'R_EX_cobalt2_e__mod1':(-100,0), 'R_EX_cl_e__mod1':(-100,0),
                   'R_EX_o2_e_':(-100,0), 'R_EX_mobd_e__mod1':(-100,0), 'R_EX_k_e_':(-100,0), 'R_EX_nh4_e_':(-100,0), 'R_EX_mg2_e__mod1':(-100,0), 'R_EX_fe3_e__mod1':(-100,0),
                   'R_EX_zn2_e__mod1':(-100,0), 'R_EX_ca2_e__mod1':(-100,0), 'R_EX_pi_e_':(-100,0), 'R_EX_cu2_e__mod1':(-100,0),
                   'R_EX_glc_D_e_':(-100, -10), 'R_t_M_glc_D_e_Extra_organism_mod1_default': (0,0),'R_PDH_mod1': (0,0)}


    for r in model2.reactions.keys():
        if r == 'R_EX_xyl_D_e_':
            print("stop")
            reac = model2.reactions[r]

    res  = FBA(model2, objective={"R_EX_succ_e_": 1}, constraints=constraints)

    for r, f in res.values.items():
        if f !=0:
            print (r + " --> " +str(f))
    print(res.values["R_EX_succ_e_"])
    print(res.values["R_BM_total_Synth"])

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
    #cbm_simualtion_iAF()

    sophia_test()


    #SBML_MODEL = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/TinyModel_RHS.xml"

    #SBML_MODEL = '../../../examples/models/Millard2016_suc_drain.xml'
    #SBML_MODEL = '../../../examples/models/Jahan2016_chemostat_fixed.xml'
    #SBML_MODEL = '../../../examples/models/chassagnole2002.xml'
    #load Model
    #model = load_kinetic_model(SBML_MODEL)

    # wild-type simulation
    result = kinetic_simulation(model)
    #result.print()
    # Change parameters
    #result = steady_state_simulation(model, parameters={'Dil': 0.2 / 3600})
    #print_simul_result(result)
    #
    # #Knockouts (the local parameters has the sufix of reactioId)
    # result = steady_state_simulation(model, factors={'vG6PDH_rmaxG6PDH': 0.0})
    # print_simul_result(result)
    #
    # # Under/over expression (the local parameters has the sufix of reactioId)
    # result = steady_state_simulation(model, factors={'vG6PDH_rmaxG6PDH': 2.0})
    # print_simul_result(result)
