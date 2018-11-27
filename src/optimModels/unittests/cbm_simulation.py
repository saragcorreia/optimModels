from optimModels.model.kineticModel import load_kinetic_model
from framed.cobra.simulation import FBA, pFBA
from framed.io.sbml import load_cbmodel
from optimModels.simulation.simul_problems import StoicSimulationProblem, KineticSimulationProblem
from optimModels.simulation.override_simul_problem import  OverrideKineticSimulProblem
from optimModels.utils.utils import fix_exchange_reactions_model

##################################################################################
# File used to validate some of the results obtained in the optimization process #
##################################################################################

# Simulation:
# model: comunity model
# objective: Maximize succinate production with a biomass >0.55
def medium_test():
    SBML_FILE = "../../../examples/models/EC_SC_model.xml"
    model = load_cbmodel(SBML_FILE)
    model2 = fix_exchange_reactions_model(model)

    for r in model2.reactions:
        print (r)

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

# Simulation:
# model: Ec_iAF1260
# objective: Maximize succinate production with a biomass >0.55
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


# Simulation:
# model: iMM904
# objective: Ethanol production with medium definition (other uptake reactions are defined in the model) and limit of biomass production
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
    medium_test()
