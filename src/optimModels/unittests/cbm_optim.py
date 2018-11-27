from cobra.io import read_sbml_model
from framed.io.sbml import load_cbmodel
from optimModels.optimization.evaluation_functions import build_evaluation_function
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.optimization.run import cbm_strain_optim
from optimModels.utils.constantes import optimType
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.utils import fix_exchange_reactions_model

basePath = "C:/Users/sara/UMinho/Projects/DeCaF/Optimizations/"
LEVELS = [1e-3, 1e-2, 1e-1, 0.5, 1, 5, 10, 50, 1e2, 5e2, 1e3, 1e4]

"""
This file contains several functions to perform different strain design strategies using stoichiometric models

"""


# Optimization:
# model: Ec_iAF1260
# Obj Func: TargetFlux (Ec_biomass_iAF1260_core_59p81M)
# type: Reaction Knockouts

def reac_ko_optim(isMultiProc=False, size=1, withCobraPy=False):
    SBML_FILE = "../../../examples/models/Ec_iAF1260.xml"
    if withCobraPy:
        model = read_sbml_model(SBML_FILE)
        fileRes = basePath + "Results/optim_Ec_iAF1260_ko_cobra.csv"
    else:
        model = load_cbmodel(SBML_FILE, flavor="cobra")
        fileRes = basePath + "Results/optim_Ec_iAF1260_ko.csv"

    simulProb = StoicSimulationProblem(model, objective={"Ec_biomass_iAF1260_core_59p81M": 1}, withCobraPy=withCobraPy)
    evalFunc = build_evaluation_function("targetFlux", ["Ec_biomass_iAF1260_core_59p81M"])
    result = cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, isMultiProc=isMultiProc,
                              candidateSize=size, resultFile=fileRes)  # KO_Reaction by default
    result.print()

# Optimization:
# model: iMM904
# Obj Func: Minimum number of reaction (MinNumberReac with production of R_EX_etoh_e)
# type: find best medium composition

def medium_SC_Etanol_optim(isMultiProc=False, size=1, withCobraPy=False):
    SBML_FILE = "../../../examples/models/iMM904.xml"

    model = load_cbmodel(SBML_FILE, flavor="fbc2")
    fileRes = basePath + "Results/optim_iMM904_etanol.csv"
    simulProb = StoicSimulationProblem(model, objective={"R_BIOMASS_SC5_notrace": 1},
                                       withCobraPy=withCobraPy)
    fba = simulProb.simulate()
    print("Biomass: " + str(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"]))

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
    simulProb.constraints.update(
        {"R_BIOMASS_SC5_notrace": (fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"] * 0.75, 9999)})

    minObjective = {"R_EX_etoh_e": 1e-5}

    print("Biomass: " + str(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"] * 0.75))

    evalFunc = build_evaluation_function("MinNumberReac", size, minObjective)

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM,
                     criticalReacs=criticalReacs, isMultiProc=isMultiProc,
                     candidateSize=size, resultFile=fileRes)  # KO_Reaction by default

# Optimization:
# model: iMM904
# Obj Func: Minimum number of uptake reactions with lower levels that maximizes the production of target compound (MinNumberReacAndMaxFluxWithLevels with production of R_EX_etoh_e)
# type: find best medium composition

def medium_SC_Etanol_Levels_optim(isMultiProc=False, size=1, withCobraPy=False):
    SBML_FILE = "../../../examples/models/iMM904.xml"

    model = load_cbmodel(SBML_FILE, flavor="fbc2")
    fileRes = basePath + "Results/optim_iMM904_etanol_levels.csv"
    simulProb = StoicSimulationProblem(model, objective={"R_BIOMASS_SC5_notrace": 1},
                                       withCobraPy=withCobraPy)
    fba = simulProb.simulate()
    print("Biomass: " + str(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"]))
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
    simulProb.constraints.update(
        {"R_BIOMASS_SC5_notrace": (fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"] * 0.75, 9999)})

    print("Biomass: " + str(fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"] * 0.75))

    evalFunc = build_evaluation_function("MinNumberReacAndMaxFluxWithLevels", size, LEVELS,
                                         {"R_EX_etoh_e": model.reactions["R_EX_etoh_e"].ub})

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=LEVELS, type=optimType.MEDIUM_LEVELS,
                     criticalReacs=criticalReacs, isMultiProc=isMultiProc,
                     candidateSize=size, resultFile=fileRes)

# Optimization:
# model: iMM904
# Obj Func: Minimum number of reaction (MinNumberReac with at least 0.75 of WT growth)
# type: find best medium composition

def medium_SC_optim(isMultiProc=False, size=1, withCobraPy=False):
    SBML_FILE = "../../../examples/models/iMM904.xml"
    model = load_cbmodel(SBML_FILE, flavor="fbc2")
    fileRes = basePath + "Results/optim_iMM904_medium.csv"

    simulProb = StoicSimulationProblem(model, objective={"R_BIOMASS_SC5_notrace": 1}, withCobraPy=withCobraPy)

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
    minObjective = {"R_BIOMASS_SC5_notrace": fba.get_fluxes_distribution()["R_BIOMASS_SC5_notrace"] * 0.75}
    evalFunc = build_evaluation_function("MinNumberReac", size, minObjective)

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM,
                     criticalReacs=criticalReacs, isMultiProc=isMultiProc, candidateSize=size, resultFile=fileRes)

# Optimization:
# model: Ec_iAF1260
# Obj Func: Minimum number of reaction (MinNumberReac with at least 0.75 of WT growth)
# type: find best medium composition
def medium_optim(isMultiProc=False, size=1, withCobraPy=False):
    SBML_FILE = "../../../examples/models/Ec_iAF1260.xml"
    if withCobraPy:
        model = read_sbml_model(SBML_FILE)
        fileRes = basePath + "Results/optim_Ec_iAF1260_medium_cobra.csv"
    else:
        model = load_cbmodel(SBML_FILE, flavor="cobra")
        fileRes = basePath + "Results/optim_Ec_iAF1260_medium.csv"

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

    minObjective = {
        "R_Ec_biomass_iAF1260_core_59p81M": fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"] * 0.75}
    evalFunc = build_evaluation_function("MinNumberReac", size, minObjective)

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM,
                     criticalReacs=criticalReacs, isMultiProc=isMultiProc, candidateSize=size,
                     resultFile=fileRes)  # KO_Reaction by default

# Optimization:
# model: Ec_iAF1260
# Obj Func: Minimum number of uptake reactions (MinNumberReac with production of a minimum of R_EX_lac_L_e)
# type: find best medium composition
def medium_Lactate_optim(isMultiProc=False, size=1, withCobraPy=False):
    SBML_FILE = "../../../examples/models/Ec_iAF1260.xml"
    modelaux = load_cbmodel(SBML_FILE, flavor="cobra")
    model = fix_exchange_reactions_model(modelaux)
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
    simulProb.constraints.update({"R_Ec_biomass_iAF1260_core_59p81M": (
    fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"] * 0.75, 9999)})

    minObjective = {"R_EX_lac_L_e": 1e-5}
    print("Biomass: " + str(fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"] * 0.75))
    build_evaluation_function
    evalFunc = build_evaluation_function("MinNumberReac", size, minObjective)

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM,
                     criticalReacs=criticalReacs, isMultiProc=isMultiProc,
                     candidateSize=size, resultFile=fileRes)

# Optimization:
# model: Ec_iAF1260
# Obj Func: Minimum number of uptake reactions with lower levels that maximizes the production of target compound (MinNumberReacAndMaxFluxWithLevels with production of R_EX_succ_e)
# type: find best medium composition
def medium_reac_ko_optim(isMultiProc=False, size=[5, 5], withCobraPy=False):
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
    simulProb.constraints.update({"R_Ec_biomass_iAF1260_core_59p81M": (
    fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"] * 0.25, 9999)})
    print("Biomass: " + str(fba.get_fluxes_distribution()["R_Ec_biomass_iAF1260_core_59p81M"] * 0.25))

    evalFunc = build_evaluation_function("MinNumberReacAndMaxFlux", sum(size),
                                         {"R_EX_succ_e": model.reactions["R_EX_succ_e"].ub})

    cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM_REACTION_KO,
                     criticalReacs=essential, isMultiProc=isMultiProc,
                     candidateSize=size, resultFile=fileRes)  # KO_Reaction by default


# Optimization:
# model: EC_SC_model (community model generated by sophia's tool)
# Obj Func: BPY (maximizes the production of succinate by the community model)
# type: reaction knockouts
def reac_ko_optim_CM(isMultiProc=False, size=1, withCobraPy=False):
    SBML_FILE = basePath + "Data/EC_SC_model.xml"
    modelaux = load_cbmodel(SBML_FILE, exchange_detection_mode="R_EX_")
    model = fix_exchange_reactions_model(modelaux)
    fileRes = basePath + "Results/optim_Comunity_KO.csv"

    for r_id, rxn in model.reactions.items():
        if r_id.startswith('R_EX_'):  # ou tambem podes fazer if rxn.is_exchange:
            rxn.lb = -1000 if rxn.lb is None else rxn.lb
            rxn.ub = 1000 if rxn.ub is None else rxn.ub

    simulProb = StoicSimulationProblem(model, objective={"R_BM_total_Synth": 1}, withCobraPy=withCobraPy)
    evalFunc = build_evaluation_function("BPCY", "R_BM_total_Synth", "R_EX_succ_medium_", "R_EX_glc_D_medium_")

    result = cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, isMultiProc=isMultiProc,
                              candidateSize=size, resultFile=fileRes)
    result.print()

# Optimization:
# model: EC_SC_model (community model generated by sophia's tool)
# Obj Func: BP_MinModifications (maximizes the production of succinate with the minimum of uptakes)
# type: find best medium compoisition and kO
def reac_ko_medium_optim_CM(isMultiProc=False, size=(1,1), withCobraPy=False):
    SBML_FILE = basePath + "Data/EC_SC_model.xml"
    modelaux = load_cbmodel(SBML_FILE, exchange_detection_mode="R_EX_")
    model = fix_exchange_reactions_model(modelaux)
    fileRes = basePath + "Results/optim_Comunity_KO_medium_pFBA.csv"

    for r_id, rxn in model.reactions.items():
        if r_id.startswith('R_EX_'):  # ou tambem podes fazer if rxn.is_exchange:
            rxn.lb = -1000 if rxn.lb is None else rxn.lb
            rxn.ub = 1000 if rxn.ub is None else rxn.ub

    simulProb = StoicSimulationProblem(model, objective={"R_BM_total_Synth": 1}, withCobraPy=withCobraPy)
    res = simulProb.simulate()
    print(res.print())
    evalFunc = build_evaluation_function("BP_MinModifications", "R_BM_total_Synth", "R_EX_succ_medium_")

    result = cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM_REACTION_KO,
                              isMultiProc=isMultiProc, candidateSize=size, resultFile=fileRes)


if __name__ == '__main__':
    import time

    size = 5

    t1 = time.time()
    # medium_SC_optim(False, size, False)
    # medium_SC_Etanol_optim (False, size, False)
    # medium_SC_Etanol_Levels_optim(False, size, False)
    # medium_optim(False, size, False)
    # reac_ko_optim_CM(False, size, False)
    reac_ko_medium_optim_CM(False, (50, 10), False)

    t2 = time.time()
    print("time of FRAMED: " + str(t2 - t1))

    t1 = time.time()
    # reac_ko_optim(False, size, True)
    t2 = time.time()
    print("time of COBRAPY: " + str(t2 - t1))
