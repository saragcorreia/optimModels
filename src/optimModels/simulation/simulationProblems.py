import time
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from numpy import linspace
from optimModels.utils.utils import merge_two_dicts

from optimModels.simulation.simulationResults import kineticSimulationResult, stoichiometricSimulationResult
from optimModels.simulation.solvers import odeSolver


class simulationProblem:
    __metaclass__ = ABCMeta

    def get_model(self):
        return self.model

    @abstractmethod
    def simulate(self, solverId):
        pass

# NOT USED .. YET
class stoichiometricSimulationProblem(simulationProblem):
    def __init__(self, model, envConditions, objFunc, method):
        self.model = model
        self.envConditions = envConditions
        self.objFunc = objFunc
        self.method = method


    # TO DO
    def simulate(self, solverId):
        print "stoichiometric model simulation!"
        print "TO DO" #SGC: using framed / CAMEO / ???
        res = stoichiometricSimulationResult(self.get_model().id, [], "FBA", OrderedDict() )





class kineticSimulationProblem(simulationProblem):
    def __init__(self, model, parameters=OrderedDict(), rDict=OrderedDict(), time = 1e9, steps = 10000, tSteps = None):
        self.model = model
        self.parameters = parameters
        self.newParameters = OrderedDict() #used in the optimization and sampling (Patricia)
        self.newFactors = OrderedDict()
        self.rDict = rDict
        self.reacsToDel = None
        self.time = time
        self.steps = steps
        self.tSteps = tSteps
        # build ODE system
        self.update_obj()

    def set_reactions_ko(self, reacsToDel = None):
        if self.reacsToDel is not None:
            self.reacsToDel.extend(x for x in reacsToDel if x not in self.reacsToDel)
        else:
            self.reacsToDel = reacsToDel
        self.newFactors.update(OrderedDict([(r_id, 0) for r_id in self.reacsToDel]))

    def reset_parameters(self):
        self.newParameters = OrderedDict()
        self.newFactors = OrderedDict()
        self.reacsToDel = None

    def set_parameters(self, parameters):
        self.newParameters.update(parameters)

    def get_parameters(self):
        return merge_two_dicts(self.parameters, self.newParameters)

    def set_factors(self, newFactors):
        self.newFactors.update(newFactors)

    def get_factors(self):
        return self.newFactors.copy()

    def update_obj(self):
        self.f = self.model.get_ode(r_dict=self.rDict, params=merge_two_dicts(self.parameters, self.newParameters), newFactors = self.newFactors)

    def get_initial_concentrations(self):
        return self.model.concentrations.values()

    def get_time_steps(self):
        if self.tSteps is None:
            self.tSteps = linspace(0, self.time, self.steps)
        return self.tSteps

    def get_number_reactions(self):
        return len(self.model.reactions)

    def get_r_dict(self):
        return self.rDict.copy()

    def func (self, x, t):
        #f2 = lambda x, t: self.f(t, x)
        return self.f(t,x)

    def simulate(self, solverId):
        solver = odeSolver(solverId).get_solver(self)
        solver.set_initial_condition(self.get_initial_concentrations())
        t1 = time.time()
        #print self.get_time_steps()

        X, t = solver.solve(self.get_time_steps())

        #t2 = time.time()
        #print "TIME (seconds): " + str(t2 - t1)

        res = kineticSimulationResult(self.get_model().id, self.get_r_dict(),
                                      self.get_parameters(), self.get_factors(),
                                      self.get_time_steps()[len(self.get_time_steps()) - 1])

        return res
