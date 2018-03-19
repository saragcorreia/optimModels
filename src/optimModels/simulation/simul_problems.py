import time
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from framed.cobra.simulation import FBA, MOMA, ROOM, pFBA, lMOMA
from framed.solvers import solver_instance, set_default_solver

from optimModels.utils.utils import MyPool
from optimModels.simulation.simul_results import kineticSimulationResult, StoicSimulationResult
from optimModels.simulation.solvers import odespySolver
from optimModels.utils.configurations import KineticConfigurations, StoicConfigurations, SolverConfigurations
from optimModels.utils.constantes import solverStatus

try:
    import cPickle as pickle
except ImportError:
    import pickle


class SimulationProblem:
    __metaclass__ = ABCMeta

    def __init__(self, model, solverId, method):
        self.model = model
        self.solverId = solverId
        self.method = method

    @abstractmethod
    def simulate(self, overrideSimulProblem=None):
        return

    def get_model(self):
        return self.model

    def get_solver_id(self):
        return self.solverId

    def get_method(self):
        return self.method


class StoicSimulationProblem(SimulationProblem):
    """
        This class contains all required information to perform a simulation of a stoichiometric metabolic model.

        Attributes
        ------------------
        model : CBMModel
            Metabolic model object.
        objective : dict
            objective coefficients (optional)
        minimize: bool
            minimize objective function (False by default)
        constraints: dict
            environmental or additional constraints (optional)
        solverId: str
            solver id ("cplex" or "gurobi")
        method: str
            method can be "FBA", "pFBA", "MOMA", "lMOMA" and "ROOM"
    """

    def __init__(self, model, objective=None, minimize=False, constraints=None, solverId=StoicConfigurations.SOLVER,
                 method=StoicConfigurations.SOLVER_METHOD,  withCobraPy = False):
        self.withCobraPy= withCobraPy
        if self.withCobraPy:
            model.objective = next(iter(objective.keys()))
            model.solver = solverId
            if constraints:
                for rId in list(constraints.keys()):
                    reac = model.reactions.get_by_id(rId)
                    reac.bounds(constraints.get(rId)[0], constraints.get(rId)[1])
        else:
            set_default_solver(solverId)
            #self.solver = solver_instance(model)
        self.constraints = constraints
        self.objective = objective
        self.minimize = minimize
        super().__init__(model, solverId, method)

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def get_drains(self):
        if self.withCobraPy:
            reacs = [r.id for r in self.model.exchanges]
        else:
            reacs= list(self.model.get_exchange_reactions())
        return reacs

    def get_uptake_reactions(self):
        if self.withCobraPy:
            #TODO: validar as reversiveis no cobrapy
            reacs = [r.id for r in self.model.exchanges if self.model.reactions.get_by_id(r.id).lb<0]

        else:
            drains = list(self.model.get_exchange_reactions())

            reacs = [r for r in drains if self.model.reactions[r].reversible or
                     (self.model.reactions[r].lb<0 and (self.model.reactions[r].get_substrates())>0)or
                     (self.model.reactions[r].ub> 0 and (self.model.reactions[r].get_products())>0)]
        return reacs

    def get_internal_reactions(self):
        if self.withCobraPy:
            l1 = [r.id for r in self.model.reactions]
            l2 = [r.id for r in self.model.exchanges]
            reacs = set(l1) - set(l2)
        else:
            reacs= set(self.model.reactions.keys()) - set(self.model.get_exchange_reactions(include_sink=True))
        return list(reacs)

    def get_reactions_ids(self):
        if self.withCobraPy:
            reacs = [r.id for r in self.model.reactions]
        else:
            reacs= self.model.reactions.keys()
        return reacs

    def get_bounds(self, rId):
        if self.withCobraPy:
            return self.model.reactions.get_by_id(rId).lower_bound,self.model.reactions.get_by_id(rId).upper_bound
        else:
            return self.model.get_flux_bounds(rId)

    def get_constraints_reacs(self):
        return self.constraints.keys()

    def set_objective_function (self, objective):
        self.objective = objective

    def find_essential_drains(self):
        drains = self.get_drains()
        if self.constraints:
            constraints = {d:(StoicConfigurations.DEFAULT_LB, StoicConfigurations.DEFAULT_UB) for d in drains if d not in self.constraints.keys()}
        else:
            constraints = {d: (StoicConfigurations.DEFAULT_LB, StoicConfigurations.DEFAULT_UB) for d in drains}
        solution = FBA(self.model, objective=self.objective, minimize=self.minimize, constraints=constraints)

        # #which objetive reactions has flux whem drains are all open
        hasFlux = []
        for rId in self.objective.keys():
            if solution.values[rId] > 0:
                hasFlux.append(rId)

        # close each drain and check if the objective reactions have flux
        essential = []
        for d in drains:
            constraints[d] = (0,StoicConfigurations.DEFAULT_UB)
            solution = FBA(self.model, objective=self.objective, minimize=self.minimize, constraints=constraints)
            #TODO check what happens if the objective flux is negative .... minimize problem
            if (any([solution.values[rId]==0 for rId in hasFlux])):
                essential.append(d)
            constraints[d] = (StoicConfigurations.DEFAULT_LB, StoicConfigurations.DEFAULT_UB)

        return essential




    def simulate(self, overrideSimulProblem=None):
        """
        This method preform the phenotype simulation of the stoichiometric model, using the solver method and applying the modifications present in the instance of overrideSimulProblem.

        Parameters
        -----------
        overrideProblem : overrideStoicSimulProblem
            Modification over the Stoichiometric model and the default constrains.

        Returns
        --------
        out : StoicSimulationResult
            Returns an object of type StoicSimulationResult with the steady-state flux distribution.
        """
        new_constraints = OrderedDict()
        if overrideSimulProblem is not None:
            new_constraints = overrideSimulProblem.get_modifications()

        if self.constraints is not None:
            new_constraints.update(self.constraints)

        if self.withCobraPy:
            status, fluxDist = _run_stoic_simutation_with_cobra(self.model,
                                                                constraints=new_constraints)
        else:
            status, fluxDist = _run_stoic_simutation(self.model, objective=self.objective, minimize=self.minimize,
                                                     constraints=new_constraints, method=self.method)
        return StoicSimulationResult(self.model.id, solverStatus=status, ssFluxesDistrib=fluxDist,
                                     overrideSimulProblem=overrideSimulProblem)


class KineticSimulationProblem(SimulationProblem):
    """
        This class contains all required information to perform a simulation of a kinetic metabolic model.

        Attributes
        ------------------
        model : kineticModel
            Metabolic model object.
        parameters : dict (optional)
            New values for the parameters present in the model.
        t_steps : list
            list of exact time steps to evaluate (default: [0,1e9])
        timeout : int
            Maximum time in secounds allowed to perform the simulation.

    """

    def __init__(self, model, parameters=None, tSteps=[0, 1e9], timeout=KineticConfigurations.SOLVER_TIMEOUT,
                 solver=KineticConfigurations.SOLVER, method=KineticConfigurations.SOLVER_METHOD):
        self.parameters = parameters
        self.tSteps = tSteps
        self.timeout = timeout
        super().__init__(model, solver, method)

    def __getstate__(self):
        state = OrderedDict(self.__dict__.copy())
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def get_initial_concentrations(self):
        return self.model.concentrations

    def get_time_steps(self):
        return self.tSteps

    def simulate(self, overrideSimulProblem=None):
        """
        This method preform the phenotype simulation of the kinetic model, using the solverId method and applying the modifications present in the instance of overrideSimulProblem.

        Parameters
        -----------
        overrideProblem : overrideKineticSimProblem
            Modification over the kinetic model.

        Returns
        --------
        out : kineticSimulationResult
            Returns an object of type kineticSimulationResult with the steady-state flux distribution and concentrations.
        """

        final_factors = {}
        if overrideSimulProblem:
            final_factors = overrideSimulProblem.factors
        # update initial concentrations when a [enz] is changed: == 0, up or down regulated
        initConcentrations = self.get_initial_concentrations().copy()
        # print "------conc ----"
        # print initConcentrations
        # print "------conc ----"
        t1 = time.time()
        if self.timeout is None:
            status, sstateRates, sstateConc = _my_kinetic_solve(self.get_model(), self.parameters,
                                                                final_factors,
                                                                initConcentrations,
                                                                self.get_time_steps())
        else:
            p = MyPool(processes=1)
            res = p.apply_async(_my_kinetic_solve, (
                self.get_model(), self.parameters, final_factors, initConcentrations,
                self.get_time_steps()))
            try:
                status, sstateRates, sstateConc = res.get(self.timeout)  # Wait timeout seconds for func to complete.
            except Exception:
                print("Aborting due to timeout")
                sstateRates = {}
                sstateConc = {}
                status = solverStatus.ERROR
                p.terminate()
            p.close()
            p.join()
        t2 = time.time()
        #print("TIME (seconds) simulate: " + str(t2 - t1))

        return kineticSimulationResult(self.model.id, solverStatus=status, ssFluxesDistrib=sstateRates,
                                       ssConcentrations=sstateConc,
                                       overrideSimulProblem=overrideSimulProblem)


## auxiliar functions
def _run_stoic_simutation(model, objective, minimize, constraints, method):
    #import time
    #t1 = time.time()
    if method == 'FBA':
        solution = FBA(model, objective=objective, minimize=minimize, constraints=constraints)
    elif method == 'pFBA':
        solution = pFBA(model, objective=objective, minimize=minimize, constraints=constraints)
    # elif method == 'MOMA':
    #     solution = MOMA(model, objective=objective, minimize=minimize, constraints=constraints, solver=solver)
    # elif method == 'lMOMA':
    #     solution = lMOMA(model, objective=objective, minimize=minimize, constraints=constraints, solver=solver)
    # elif method == 'ROOM':
    #     solution = ROOM(model, objective=objective, minimize=minimize, constraints=constraints, solver=solver)
    else:
        raise Exception(
            "Unknown method to perform the simulation.")
    #time = str(time.time() - t1)
    #print("simulation time ", time)
    return solution.status, solution.values


def _run_stoic_simutation_with_cobra(model, constraints):
    import time
    t1= time.time()
    with model:
        for rId in list(constraints.keys()):
            reac = model.reactions.get_by_id(rId)
            reac.bounds=(constraints.get(rId)[0], constraints.get(rId)[1])
        solution = model.optimize()
    time = str(time.time() - t1)
    #print("simulation time ", time)
    return solverStatus.OPTIMAL, solution.fluxes

def _my_kinetic_solve(model, finalParameters, finalFactors, initialConc, timePoints):
    """
    Private function: auxiliary function required to avoid the pickling the solver.solve function

    """
    finalRates = OrderedDict()
    f = model.get_ode(r_dict=finalRates, params=finalParameters, factors=finalFactors)
    func = lambda x, t: f(t, x)

    solver = odespySolver(KineticConfigurations.SOLVER_METHOD).get_solver(func)
    solver.set_initial_condition(list(initialConc.values()))
    try:
        X, t = solver.solve(timePoints)
    except Exception:
        print("Error on solver!!!")
        # print X
        # print finalRates
        return {}, {}, solverStatus.ERROR

    #print(finalRates)
    # values bellow solver precision will be set to 0
    finalRates.update({k: 0 for k, v in finalRates.items() if
                       v < SolverConfigurations.ABSOLUTE_TOL and v > - SolverConfigurations.ABSOLUTE_TOL})
    conc = OrderedDict(zip(model.metabolites.keys(), X[1]))
    return solverStatus.OPTIMAL, finalRates, conc
