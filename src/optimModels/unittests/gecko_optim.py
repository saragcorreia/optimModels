
from cobra.io import read_sbml_model
from framed.io.sbml import load_cbmodel
from geckopy import GeckoModel
from optimModels.optimization.evaluation_functions import build_evaluation_function
from optimModels.simulation.simul_problems import GeckoSimulationProblem
from optimModels.optimization.run import gecko_strain_optim
from optimModels.utils.configurations import GeckoConfigurations


basePath = "C:/Users/sara/UMinho/Projects/DeCaF/Optimizations/"
LEVELS = [1e-3, 1e-2, 1e-1, 0.5, 1 , 5, 10, 50, 1e2, 5e2, 1e3, 1e4]

# Optimization:
# model: Ec_iAF1260
# Obj Func: BPCY
# type: Protein Knockouts

def prot_ko_optim (prot_measure_fractions =None, prot_measure_ggdw= None,  constraints = None, isMultiProc=False, size=1):

    #load model
    if prot_measure_fractions is None and prot_measure_ggdw is None:
        model = GeckoModel("single-pool")
    else:
        model = GeckoModel("multi-pool")
        if prot_measure_fractions:
            model.limit_proteins(fractions=prot_measure_fractions)
        else:
            model.limit_proteins(ggdw=prot_measure_ggdw)

    fileRes = basePath + "Results/optim_KO_Gecko_Yeast_SUCC_max5_scale.csv"

    simulProb = GeckoSimulationProblem(model, constraints= constraints)
    evalFunc = build_evaluation_function("BPCY", "r_2111", "r_2056", "r_1714_REV") # max succ exchange
    gecko_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes) #KO_Reaction by default

if __name__ == '__main__':
    import time
    size = 5

    t1 = time.time()
    prot_ko_optim(size = 5)

