from geckopy import GeckoModel
from optimModels.simulation.simul_problems import GeckoSimulationProblem

import pandas
import random

def protein_ko (prot_measure_fractions = None, prot_measure_ggdw = None, constraints = None):

    if prot_measure_fractions is None and prot_measure_ggdw is None:
        model = GeckoModel("single-pool")
    else:
        model = GeckoModel("multi-pool")
        if prot_measure_fractions:
            model.limit_proteins(fractions=prot_measure_fractions)
        else:
            model.limit_proteins(ggdw=prot_measure_ggdw)

    if constraints:
        for r in constraints.keys():
            model.reactions.get_by_id(r).lower_bound = constraints[r][0]
            model.reactions.get_by_id(r).upper_bound = constraints[r][1]
    res = model.optimize()






def increase_bounds():
    model = GeckoModel("single-pool")
    model.solver = 'cplex'
    for r in model.exchanges:
        r.upper_bound = r.upper_bound * 100

    pool = model.reactions.get_by_id("prot_pool_exchange")
    pool.upper_bound = pool.upper_bound*1000000

    #model.p_base = 4005
    #model.constrain_pool()
    #model.limit_proteins( p_base=4005) # x 1E4
    #for r in model.exchanges:
    #    print (r.id + ": " + str(r.lower_bound) + " , " + str(r.upper_bound))
    #print (len(model.exchanges))

    print("antes"+ str(model.reactions.get_by_id("r_1663").upper_bound))
    res = model.optimize()
    print("after" + str(model.reactions.get_by_id("r_1663").upper_bound))

    print("growth "+ str(res.objective_value))
    a = res.fluxes
    for k,v in res.fluxes.items():
        if k.startswith("draw_prot_") or k.startswith("prot_pool_exchange"):
            print(k +"  -> "+str(v))



def simulate_prot():
    model = GeckoModel("single-pool")
    model.solver = 'cplex'

    with model:
 #       for p in ["P53685","Q01574"]:
        for p in ['P33421']:
            r = model.reactions.get_by_id("draw_prot_" + p)
            r.lower_bound = 0
            r.upper_bound = 0
        res = model.optimize()
        print(" --> growth "+ str(res.objective_value))
        print (" --> r_2111 "+ str(res.fluxes["r_2111"]))
        print(" --> r_2056 " + str(res.fluxes["r_2056"]))
        print (" --> r_1714 "+ str(res.fluxes["r_1714_REV"]))


    print(" ------------ ")

def simulate_wt ():
    model = GeckoModel('single-pool')
    res = model.optimize()
    print (res)
    #for p in model.proteins:
    p= "P38066"
    with model:
        r = model.reactions.get_by_id("draw_prot_" + p)

        lb = r.lower_bound
        ub = r.upper_bound
        r.lower_bound = 0
        r.upper_bound = 0.000001
        res = model.optimize()

        #r.knock_out()
        #res = model.optimize()
        print( p + " wt simulation1 " + str(res.objective_value))

    print (str(r.lower_bound) +" --> " +  str(r.upper_bound))

def simulate_wt_multi ():
    model = GeckoModel('multi-pool')
    import pandas
    some_measurements = pandas.Series({'P00549': 0.1, 'P31373': 0.1, 'P31382': 0.1})
    model = GeckoModel('multi-pool')
    model.limit_proteins(some_measurements)
    res = model.optimize()

    print(" wt simulation1 " , res.objective_value)
    for r in model.reactions:
        print (r.id," --> " ,res.fluxes[r.id])



def analysis_growth (resFileName):
    levels = [0,1e-10,1e-8,1e-6,1e-4,1e-2,0.1]
    model =  GeckoModel('single-pool')
    proteins = model.proteins
    df = pandas.DataFrame(index=proteins, columns=levels)

    for p in proteins:
        print (p)
        if p !="P38066":
            for level in levels:
                r = model.reactions.get_by_id("draw_prot_" + p)
                lb = r.lower_bound
                ub = r.upper_bound
                r.lower_bound = 0
                r.upper_bound =  level
                res = model.optimize()
                df.loc[p][level]= res.objective_value
                r.lower_bound = lb
                r.upper_bound = ub
    df.to_csv(resFileName)

def analysis_ko (resFileName):
    levels = [0,1e-10,1e-8,1e-6,1e-4,1e-2,0.1]

    model =  GeckoModel('single-pool')
    df = pandas.DataFrame(index = range(100), columns=["ko", "Biomass"])

    for i in range(100):
        proteins = random.sample(model.proteins,10)
        dic = {p:0 for p in proteins}
        model.limit_proteins(pandas.Series(dic))
        res = model.optimize()
        df.loc[i]= (dic, res.objective_value)
    df.to_csv(resFileName)




if __name__ =="__main__":
    #simulate_wt()
    #increase_bounds()
    #simulate_wt_multi()
    simulate_prot()
    fileRes = "C:/Users/sara/UMinho/Projects/DeCaF/GECKO_results/growth_variance.csv"
    #analysis_growth(fileRes)

    fileRes = "C:/Users/sara/UMinho/Projects/DeCaF/GECKO_results/growth_KO_10.csv"
   # analysis_ko(fileRes)

#if __name__ =="__main__":
#    import time
#    import random

 #   some_measurements = pandas.Series({'P32377': 0})
 #   model = GeckoModel('single-pool')
   # model.limit_proteins(some_measurements)
  #  res = model.optimize()
  #  values = {k: v for k, v in res.fluxes.items() if k.startswith("draw_")}
   # print(values)
