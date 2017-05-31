import copy

from optimModels.simulation.solvers import odespySolver
from optimModels.simulation.overrideSimulationProblem import overrideKineticSimulProblem
from pandas import  read_csv
from collections import OrderedDict

from optimModels.model.dynamicModel import load_kinetic_model

class MissingParams(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def simplify_solutions(odeProblem, fileRes, fileFinalRes, objFunc, solverId = odespySolver.LSODA):
    file = open(fileRes, 'r')
    data = read_csv(fileRes, sep=';', header=2)
    maxGen = max(data['Generation'])
    data2 = data.loc[data['Generation']==maxGen,]
    data2 = data2.iloc[:,0:4]

    for i in range(data2.shape[0]):
        solution = eval(data2.iloc[i,3])
        solutionIndex = list((eval(data2.iloc[i,2])))
        finalSolutionIndex= copy.copy(solutionIndex)
        finalSolution = copy.copy (solution)
        fitness = data2.iloc[i,1]

        # do not simplify solutions with fitness == 0 and with a single modification
        if fitness > 0.0 and len(solution)>1:
            # intSetRep
            if isinstance( list(solutionIndex)[0], int ):
                desv = 0
                for j in range(len(solution)):
                    elem = solution[j]
                    ko_to_test = copy.copy(finalSolution)
                    ko_to_test.remove(elem)
                    if not _required_ko_reaction(odeProblem, ko_to_test, fitness, objFunc, solverId):
                        print  str(j)+ " simplification " + str(solution)
                        finalSolution.pop(j-desv)
                        finalSolutionIndex.pop(j-desv)
                        desv = desv + 1
            else:
                desv = 0
                for j in range(len(solution)):
                    elem = solution.items()[j]
                    tuples_to_test = copy.copy(finalSolution)
                    del tuples_to_test[elem[0]]
                    if not _required_under_over(odeProblem, tuples_to_test, fitness, objFunc, solverId):
                        print  str(j) + " simplification " + str(solution)

                        del finalSolution[elem[0]]
                        finalSolutionIndex.pop(j-desv)
                        desv = desv + 1
            data2.iloc[i, 2] = str(finalSolutionIndex)
            data2.iloc[i, 3] = str(finalSolution)
    file.close()
    #save new data
    data2.to_csv( path_or_buf = fileFinalRes, sep=";", index=False)



def _required_ko_reaction (odeProblem, ko, fitness, foReac, solverId):
    koFactors=[(elem, 0) for elem in ko]
    #print koFactors
    override = overrideKineticSimulProblem(factors=koFactors)
    try:
        res = odeProblem.simulate(solverId, override)
        newFitness = res.get_fluxes_distribution()[foReac]
    except Exception:
        newFitness = -1.0
    return round(fitness, 12) != round(newFitness, 12)

def _required_under_over(odeProblem, tuples, fitness, foReac, solverId):
    #print tuples
    override = overrideKineticSimulProblem(factors = tuples)
    try:
        res = odeProblem.simulate(solverId, override)
        newFitness = res.get_fluxes_distribution()[foReac]
    except Exception:
        newFitness = -1.0
    print str(tuples) + " --> " + str(fitness) + " -->"+ str(newFitness)
    return round(fitness, 12) != round(newFitness, 12)
