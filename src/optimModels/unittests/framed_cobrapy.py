from framed.io.sbml import load_cbmodel

from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.optimization.evaluation_functions import build_evaluation_function
from optimModels.optimization.run import cbm_strain_optim

from cobra.io import read_sbml_model

#from cameo.strain_design.heuristic.evolutionary.optimization import ReactionKnockoutOptimization
#from cameo.strain_design.heuristic.evolutionary.objective_functions import CameoTargetFlux

#from cameo.parallel import MultiprocessingView

SBML_FILE = "../../../examples/models/Ec_iAF1260.xml"
basePath = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/"


def print_results (fileName, population, optimConfig):

    file = open(fileName, 'a')
    file.write("population_size;candidate_max_size;crossover_rate; mutation_rate;new_candidates_rate; num_elites\n")
    file.write(";".join(map(str,optimConfig.get_ea_configurations().get_default_config())))
    file.write("Generation;Fitness;Candidate;Reactions\n")

    # save all candidates of the population
    for ind in population:
        solution_decoded = optimConfig.getdecoder().decode_candidate(ind.candidate)
        file.write(("{0};{1};{2};{3} \n").format(100, ind.fitness, ind.candidate, solution_decoded))
    file.close()

def framed_optim(isMultiProc, size):
    model = load_cbmodel(SBML_FILE, flavor="cobra")

    fileRes = basePath + "Results/optim_Ec_iAF1260_ko.csv"
    simulProb = StoicSimulationProblem(model, objective={"R_Ec_biomass_iAF1260_core_59p81M": 1})
    objFunc = build_evaluation_function("targetFlux", ["R_Ec_biomass_iAF1260_core_59p81M"])
    cbm_strain_optim(simulProb, evaluationFunc=objFunc, levels=None, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes)


def cobra_optim(isMultiProc, size):
    model = read_sbml_model(SBML_FILE)
    fileRes = basePath + "Results/optim_Ec_iAF1260_ko_cobra.csv"

    simulProb = StoicSimulationProblem(model, objective={"Ec_biomass_iAF1260_core_59p81M": 1}, withCobraPy=True)
    objFunc = build_evaluation_function("targetFlux", ["Ec_biomass_iAF1260_core_59p81M"])

    print ( simulProb.simulate())
    cbm_strain_optim(simulProb, evaluationFunc=objFunc, levels=None, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes)

#
def print_drains_cobrapy():
    model = read_sbml_model(SBML_FILE)
    for r in model.exchanges:
        print (r.id + str(model.reactions.get_by_id(r.id).lower_bound) + " <---> " + str(model.reactions.get_by_id(r.id).upper_bound))



if __name__ == '__main__':
    import time
    import warnings
    import sys
    warnings.filterwarnings('ignore')  # ignore the warnings related to floating points raise from solver!!!
    size = 6
   # print_drains_cobrapy()
    t1 = time.time()
    #cameo_optim(True, size)
    t2 = time.time()
    print ("time of CAMEO: " + str(t2 - t1))

    t1 = time.time()
   #framed_optim(False, size)
    t2 = time.time()
    print ("time of FRAMED: " + str(t2 - t1))

    t1 = time.time()
    cobra_optim(False, size)
    t2 = time.time()
    print ("time of COBRAPY: " + str(t2 - t1))



# time of CAMEO: 180.13730311393738
# time of FRAMED: 119.66580080986023
# time of COBRAPY: 79.39047503471375