import copy

from optimModels.simulation.solvers import odeSolver
from pandas import  read_csv

from optimModels.model.dynamicModel import load_kinetic_model

class MissingParams(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def simplify_solutions(odeProblem, fileRes, fileFinalRes, objFunc, solverId = odeSolver.LSODA, levels=None):
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
                if levels is None:
                    raise MissingParams('Possible levels values required.')
                desv = 0
                for j in range(len(solution)):
                    elem = solution[j]
                    tuples_to_test = copy.copy(finalSolution)
                    tuples_to_test.remove(elem)
                    if not _required_under_over(odeProblem, tuples_to_test,fitness, objFunc, solverId, levels):
                        print  str(j) + " simplification " + str(solution)
                        finalSolution.pop(j-desv)
                        finalSolutionIndex.pop(j-desv)
                        desv = desv + 1
            data2.iloc[i, 2] = str(finalSolutionIndex)
            data2.iloc[i, 3] = str(finalSolution)
    file.close()

    #save new data
    data2.to_csv( path_or_buf = fileFinalRes, sep=";", index=False)



def _required_ko_reaction (odeProblem, ko, fitness, foReac, solverId):
    odeProblem.reset_parameters()
    odeProblem.set_reactions_ko(ko)
    odeProblem.update_obj()

    solver = odeSolver(solverId).get_solver(odeProblem)
    solver.set_initial_condition(odeProblem.get_initial_concentrations())

    try:
        X, t = solver.solve(odeProblem.get_time_steps())
    except ValueError, e:
        print "Oops! Solver problems.  " + e.message
        return True

    newFitness = odeProblem.get_r_dict()[foReac]
    return round(fitness, 12) != round(newFitness, 12)

def _required_under_over(odeProblem, tuples, fitness, foReac, solverId, levels):
    odeProblem.reset_parameters()
    odeProblem.set_factors(tuples)
    odeProblem.update_obj()
    solver = odeSolver(solverId).get_solver(odeProblem)
    solver.set_initial_condition(odeProblem.get_initial_concentrations())

    try:
        X, t = solver.solve(odeProblem.get_time_steps())
    except ValueError, e:
        print "Oops! Solver problems.  " + e.message
    newFitness = odeProblem.get_r_dict()[foReac]
    return round(fitness, 12) != round(newFitness, 12)


if __name__ == '__main__':
    dirResults = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Results/"
    sizes=[1,2,3,4,5,6]

    sbmlFile =  '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'
    model = load_kinetic_model(sbmlFile)
    dils = [(0.1/3600)]

    problem = KineticSimulationProblem(model, parameters={'Dil': dils[0]}, tSteps=[0, 1e9])
    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]

    for size in sizes:
        fileRes = dirResults + 'optim_Chassagnole_Serine_size' + str(size) + '.csv'
        fileFinalRes = dirResults + 'Final_optim_Chassagnole_Serine_size' + str(size) + '.csv'
        simplify_solutions(problem, fileRes, fileFinalRes, "vsersynth")
