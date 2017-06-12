from optimModels.optimization.objectiveFunctions import build_objective_function
from optimModels.optimization.run import strain_optim

BASE_PATH ="/Volumes/Data/Documents/Projects/DeCaF/Optimizations"
SAVE_RESULT_FILE = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/optim_Chassagnole_Serine_dummy.csv"
LEVELS = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]


def ko_chassagnole():
    sbmlFile = BASE_PATH+'/Data/chassagnole2002.xml'
    fileRes = BASE_PATH +"/Results/optim_Chassagnole_Serine.csv"

    objFunc = build_objective_function("Target Flux", ["vsersynth"])

    result = strain_optim(sbmlFile, objFunc=objFunc, levels=None, criticalGenes=[], isMultiProc=False, resultFile=fileRes)
    for r in result:
        print r.print_result()


def under_over_chassagnole():
    sbmlFile = BASE_PATH+'/Data/chassagnole2002.xml'
    fileRes = BASE_PATH +"/Results/optim_Chassagnole_Serine_under.csv"

    objFunc = build_objective_function("Target Flux", ["vsersynth"])

    result = strain_optim(sbmlFile, objFunc=objFunc, levels=LEVELS, criticalGenes=[], isMultiProc=False, resultFile=fileRes)
    for r in result:
        print r.print_result()



if __name__ == '__main__':
    import time
    import warnings
    warnings.filterwarnings('ignore')  # ignore the warnings related to floating points raise from solver!!!
    t1 = time.time()
    ko_chassagnole()
    t2 = time.time()
    print "time with multiproccessing" + str(t2 - t1)
