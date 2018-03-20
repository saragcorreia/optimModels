
from cobra.io import read_sbml_model
from framed.io.sbml import load_cbmodel
from optimModels.optimization.evaluation_functions import build_evaluation_function
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.optimization.run import cbm_strain_optim
from optimModels.utils.constantes import optimType
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.utils import fix_exchange_reactions_model



SBML_FILE = "../../../examples/models/Ec_iAF1260.xml"
basePath = "C:/Users/sara/UMinho/Projects/DeCaF/Optimizations/"
LEVELS = [1e-3, 1e-2, 1e-1, 0.5, 1 , 5, 10, 50, 1e2, 5e2, 1e3, 1e4]

def reac_ko_optim (isMultiProc=False, size=1, withCobraPy = False):
    if withCobraPy:
        model = read_sbml_model(SBML_FILE)
        fileRes = basePath + "Results/optim_Ec_iAF1260_ko_cobra.csv"
    else:
        model = load_cbmodel(SBML_FILE, flavor="cobra")
        fileRes = basePath + "Results/optim_Ec_iAF1260_ko.csv"

    simulProb = StoicSimulationProblem(model, objective={"Ec_biomass_iAF1260_core_59p81M": 1}, withCobraPy=withCobraPy)
    evalFunc = build_evaluation_function("targetFlux", ["Ec_biomass_iAF1260_core_59p81M"])
    result = cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes) #KO_Reaction by default
    result.print()

def medium_SC_Etanol_optim(isMultiProc=False, size=1, withCobraPy = False):
    SBML_FILE = "../../../examples/models/iMM904.xml"

    model = load_cbmodel(SBML_FILE, flavor="fbc2")
    fileRes = basePath + "Results/optim_iMM904_etanol.csv"
    simulProb = StoicSimulationProblem(model, objective={"R_BIOMASS_SC5_notrace": 1},
                                       withCobraPy=withCobraPy)
    fba = simulProb.simulate()
    print ("Biomass: " + str(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"]))
    # calculate the essential uptake reactions to biomass production
    essential = simulProb.find_essential_drains()
    print(essential)
    if simulProb.constraints:
        simulProb.constraints.update(
            {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential})  # put essential reactions as constraints
    else:
        simulProb.constraints = {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential}

    criticalReacs = essential

    # set the minimum production of biomass
    simulProb.set_objective_function({"R_EX_etoh_e": 1})
    simulProb.constraints.update({"R_BIOMASS_SC5_notrace":(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"] * 0.75,9999)})

    minObjective = {"R_EX_etoh_e": 1e-5}

    print ("Biomass: " + str(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"] * 0.75))

    evalFunc = build_evaluation_function("MinNumberReac", size, minObjective)

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM, criticalReacs = criticalReacs, isMultiProc=isMultiProc,
                     candidateSize=size, resultFile=fileRes)  # KO_Reaction by default
################
def medium_SC_Etanol_Levels_optim(isMultiProc=False, size=1, withCobraPy = False):
    SBML_FILE = "../../../examples/models/iMM904.xml"

    model = load_cbmodel(SBML_FILE, flavor="fbc2")
    fileRes = basePath + "Results/optim_iMM904_etanol_levels.csv"
    simulProb = StoicSimulationProblem(model, objective={"R_BIOMASS_SC5_notrace": 1},
                                       withCobraPy=withCobraPy)
    fba = simulProb.simulate()
    print ("Biomass: " + str(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"]))
    # calculate the essential uptake reactions to biomass production
    essential = simulProb.find_essential_drains()
    print(essential)
    if simulProb.constraints:
        simulProb.constraints.update(
            {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential})  # put essential reactions as constraints
    else:
        simulProb.constraints = {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential}

    criticalReacs = essential

    # set the minimum production of biomass
    simulProb.set_objective_function({"R_EX_etoh_e": 1})
    simulProb.constraints.update({"R_BIOMASS_SC5_notrace":(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"] * 0.75,9999)})

    print ("Biomass: " + str(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"] * 0.75))

    evalFunc = build_evaluation_function("MinNumberReacAndMaxFluxWithLevels", size, LEVELS, {"R_EX_etoh_e": model.reactions["R_EX_etoh_e"].ub})

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=LEVELS, type=optimType.MEDIUM_LEVELS, criticalReacs = criticalReacs, isMultiProc=isMultiProc,
                     candidateSize=size, resultFile=fileRes)  # KO_Reaction by default
################
def medium_SC_optim (isMultiProc=False, size=1, withCobraPy = False):
    SBML_FILE = "../../../examples/models/iMM904.xml"
    model = load_cbmodel(SBML_FILE, flavor="fbc2")
    fileRes = basePath + "Results/optim_iMM904_medium.csv"

    simulProb = StoicSimulationProblem(model, objective = {"R_BIOMASS_SC5_notrace":1}, withCobraPy = withCobraPy)

    fba = simulProb.simulate()

    # calculate the essential uptake reactions to biomass production
    essential = simulProb.find_essential_drains()
    print(essential)
    if simulProb.constraints:
        simulProb.constraints.update(
            {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential})  # put essential reactions as constraints
    else:
        simulProb.constraints = {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential}

    criticalReacs = essential

    # set the minimum production of biomass


    minObjective = {"R_BIOMASS_SC5_notrace": fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"]* 0.75}
    evalFunc = build_evaluation_function("MinNumberReac",size, minObjective)

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type = optimType.MEDIUM, criticalReacs = criticalReacs, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes)

def medium_optim (isMultiProc=False, size=1, withCobraPy = False):
    SBML_FILE = "../../../examples/models/Ec_iAF1260.xml"
    if withCobraPy:
        model = read_sbml_model(SBML_FILE)
        fileRes = basePath + "Results/optim_Ec_iAF1260_medium_cobra.csv"
    else:
        model = load_cbmodel(SBML_FILE, flavor="cobra")
        fileRes = basePath + "Results/optim_Ec_iAF1260_medium.csv"

    simulProb = StoicSimulationProblem(model, objective = {"R_Ec_biomass_iAF1260_core_59p81M":1}, withCobraPy = withCobraPy)

    fba = simulProb.simulate()

    # calculate the essential uptake reactions to biomass production
    essential = simulProb.find_essential_drains()
    print(essential)
    if simulProb.constraints:
        simulProb.constraints.update(
            {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential})  # put essential reactions as constraints
    else:
        simulProb.constraints = {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential}

    criticalReacs = essential

    # set the minimum production of biomass


    minObjective = {"R_Ec_biomass_iAF1260_core_59p81M": fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"]* 0.75}
    evalFunc = build_evaluation_function("MinNumberReac",size, minObjective)

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type = optimType.MEDIUM, criticalReacs = criticalReacs, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes) #KO_Reaction by default

def medium_Lactate_optim(isMultiProc=False, size=1, withCobraPy = False):
    SBML_FILE = "../../../examples/models/Ec_iAF1260.xml"
    model = load_cbmodel(SBML_FILE, flavor="cobra")
    fileRes = basePath + "Results/optim_Ec_iAF1260_medium_lactate.csv"
    simulProb = StoicSimulationProblem(model, objective={"R_Ec_biomass_iAF1260_core_59p81M": 1},
                                       withCobraPy=withCobraPy)

    fba = simulProb.simulate()

    # calculate the essential uptake reactions to biomass production
    essential = simulProb.find_essential_drains()
    print(essential)
    if simulProb.constraints:
        simulProb.constraints.update(
            {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential})  # put essential reactions as constraints
    else:
        simulProb.constraints = {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential}

    criticalReacs = essential

    # set the minimum production of biomass

    simulProb.set_objective_function({"R_EX_lac_L_e": 1})
    simulProb.constraints.update({"R_Ec_biomass_iAF1260_core_59p81M":(fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"] * 0.75,9999)})

    minObjective = {"R_EX_lac_L_e": 1e-5}
    print ("Biomass: " + str(fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"] * 0.75))
    build_evaluation_function
    evalFunc = build_evaluation_function("MinNumberReac",size,  minObjective)

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM, criticalReacs = criticalReacs, isMultiProc=isMultiProc,
                     candidateSize=size, resultFile=fileRes)  # KO_Reaction by default

def medium_reac_ko_optim(isMultiProc=False, size=[5,5], withCobraPy = False):
    SBML_FILE = "../../../examples/models/Ec_iAF1260.xml"
    model = load_cbmodel(SBML_FILE, flavor="cobra")
    newModel = fix_exchange_reactions_model(model)
    fileRes = basePath + "Results/optim_Ec_iAF1260_medium_ko_succ.csv"
    simulProb = StoicSimulationProblem(newModel, objective={"R_Ec_biomass_iAF1260_core_59p81M": 1},
                                       withCobraPy=withCobraPy)

    # set the minimum production of biomass
    fba = simulProb.simulate()


    # calculate the essential uptake reactions to biomass production
    essential = simulProb.find_essential_drains()
    print(essential)
    if simulProb.constraints:
        simulProb.constraints.update(
            {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential})  # put essential reactions as constraints
    else:
        simulProb.constraints = {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential}


    simulProb.set_objective_function({"R_EX_succ_e_": 1})
    simulProb.constraints.update({"R_Ec_biomass_iAF1260_core_59p81M":(fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"] * 0.25,9999)})
    print ("Biomass: " + str(fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"] * 0.25))

    evalFunc = build_evaluation_function("MinNumberReacAndMaxFlux",sum(size) , {"R_EX_succ_e": model.reactions["R_EX_succ_e"].ub})

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM_REACTION_KO, criticalReacs = essential, isMultiProc=isMultiProc,
                     candidateSize=size, resultFile=fileRes)  # KO_Reaction by default

if __name__ == '__main__':
    import time
    size = 30

    t1 = time.time()
   # medium_SC_optim(False, size, False)
    #medium_SC_Etanol_optim (False, size, False)
    #medium_SC_Etanol_Levels_optim(False, size, False)
    #medium_optim(False, size, False)
    medium_reac_ko_optim(False, (size, 10), False)

    t2 = time.time()
    print ("time of FRAMED: " + str(t2 - t1))

    t1 = time.time()
    #reac_ko_optim(False, size, True)
    t2 = time.time()
    print ("time of COBRAPY: " + str(t2 - t1))
