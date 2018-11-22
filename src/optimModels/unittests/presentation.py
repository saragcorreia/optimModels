import pandas
from geckopy import GeckoModel
from optimModels.simulation.simul_problems import GeckoSimulationProblem
from optimModels.optimization.evaluation_functions import build_evaluation_function
from optimModels.simulation.simul_problems import GeckoSimulationProblem
from optimModels.optimization.run import gecko_strain_optim
basePath = "C:/Users/sara/UMinho/Projects/DeCaF/Optimizations/"

def essential_prot():
    model = GeckoModel("single-pool")
    model.solver = 'cplex'
    print("Essential proteins with cplex, normal model (single-pool)")
    for p in model.proteins:
        with model as m:
            r = m.reactions.get_by_id("draw_prot_" + p)
            r.lower_bound = 0
            r.upper_bound = 0
            res = m.optimize()
        if (res.objective_value <= 1e-10):
            print(p, ",", res.objective_value)


def essential_prot_scale():
    model = GeckoModel("single-pool")
    model.solver = 'cplex'
    print("Essential proteins with cplex, scale model (single-pool)")
    for r in model.reactions:
        r.lower_bound = r.lower_bound *100000
        r.upper_bound = r.upper_bound*100000

    for p in model.proteins:
        with model as m:
            r = model.reactions.get_by_id("draw_prot_" + p)
            r.lower_bound = 0
            r.upper_bound = 0
            res = model.optimize()

        print(p, ",", res.objective_value)

def analysis_growth(resFileName, scale = False):
    model =  GeckoModel('single-pool')
    model.solver = 'cplex'

    #scale model
    if scale:
        for r in model.reactions:
            r.upper_bound = r.upper_bound*100000
            r.lower_bound = r.lower_bound*100000

    proteins = model.proteins
    df = pandas.DataFrame(index=proteins, columns= range(100))
    for i in range(100):
        print (i)
        for p in proteins:
            with model as m :
                r = m.reactions.get_by_id("draw_prot_" + p)
                r.lower_bound = 0
                r.upper_bound = 0
                res = m.optimize()
                df.loc[p][i]= 0 if res.objective_value <1e-4 else 1
    df.to_csv(resFileName)

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

    fileRes = basePath + "Results/optim_KO_Gecko_Yeast_SUCC_max5.csv"

    simulProb = GeckoSimulationProblem(model, constraints= constraints)
    evalFunc = build_evaluation_function("BPCY", "r_2111", "r_2056", "r_1714_REV") # max succ exchange
    gecko_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes) #KO_Reaction by default

if __name__ == '__main__':
    #essential_prot()
    #essential_prot_scale()
    #analysis_growth("C:/Users/sara/UMinho/Projects/DeCaF/GECKO_results/analysis_essential_no_scale_10e-4.csv", scale= False)
    analysis_growth("C:/Users/sara/UMinho/Projects/DeCaF/GECKO_results/analysis_essential_scale_0.csv", scale=True)
