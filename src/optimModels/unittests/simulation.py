
from optimModels.simulation.run import kinetic_simulation


from optimModels.model.kineticModel import load_kinetic_model
from framed.cobra.simulation import FBA
from framed.io.sbml import load_cbmodel
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.utils.configurations import StoicConfigurations

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


    constraints = {'R_EX_so4_e': (-100000,0), 'R_EX_o2_e': (-50,0), 'R_EX_gam6p_e': (-10,0), 'R_EX_melib_e': (-5,0)}
    constraints.update({"R_BIOMASS_SC5_notrace":(0.21,9999)})
    res  = FBA(model, objective={"R_EX_etoh_e": 1}, constraints=constraints)
    print(res.values["R_EX_etoh_e"])
    print(res.values["R_BIOMASS_SC5_notrace"])
    print(res.values["R_EX_so4_e"])
    print(res.values["R_EX_gam6p_e"])
    print(res.values["R_EX_o2_e"])
    print(res.values["R_EX_melib_e"])


if __name__ == '__main__':
    cbm_simualtion_iAF()




    #SBML_MODEL = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/TinyModel_RHS.xml"

    #SBML_MODEL = '../../../examples/models/Millard2016v2.xml'
    #SBML_MODEL = '../../../examples/models/Jahan2016_chemostat_fixed.xml'
    SBML_MODEL = '../../../examples/models/chassagnole2002.xml'
    #load Model
    model = load_kinetic_model(SBML_MODEL)

    # wild-type simulation
    #result = kinetic_simulation(model)
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
