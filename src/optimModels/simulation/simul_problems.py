import time
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from framed.cobra.simulation import FBA, MOMA, ROOM, pFBA, lMOMA
from framed.solvers import solver_instance, set_default_solver

from optimModels.utils.utils import MyPool
from optimModels.simulation.simul_results import kineticSimulationResult, StoicSimulationResult, GeckoSimulationResult
from optimModels.simulation.solvers import odespySolver
from optimModels.utils.configurations import KineticConfigurations, StoicConfigurations, SolverConfigurations, GeckoConfigurations
from optimModels.utils.constantes import solverStatus
from cobra.util.solver import linear_reaction_coefficients

try:
    import cPickle as pickle
except ImportError:
    import pickle

class SimulationProblem:
    """
    Abstract class of simulation problem
    """
    __metaclass__ = ABCMeta

    def __init__(self, model, solverId, method):
        """
        Create a instance of a basic simulation problem.
        Args:
            model (Model): model instance ( CBModel, KineticModel or GeckoModel).
            solverId (str): solver used in the simulation.
            method: method to solve to use in phenotype prediction.
        """
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

class GeckoSimulationProblem(SimulationProblem):
    """
    This class contains all required information to perform a simulation of a Gecko metabolic model.
    """

    def __init__(self, model, objective=None, constraints=None, solverId=StoicConfigurations.SOLVER):
        """
        Create a instance of GeckoSimulProblem.

        Args:
            model (GeckoModel): Metabolic model
            objective: Objective coefficients (optional)
            constraints: Environmental conditions  or additional constraints (optional)
            solverId (str): Solver id ("cplex", "glpk", "gurobi")
        """
        if objective:
            model.objective = next(iter(objective.keys())) # only the first reac id will be set as objective function with coeficient 1
            self.objective = objective
        else:
            (reac, coef)  = next(iter(linear_reaction_coefficients(model).items()))
            self.objective = {reac.id:coef}
        model.solver = solverId
        if constraints:
            for rId in list(constraints.keys()):
                reac = model.reactions.get_by_id(rId)
                reac.bounds(constraints.get(rId)[0], constraints.get(rId)[1])

        self.constraints = constraints

        super().__init__(model, solverId, "gecko")

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def get_drains(self):
        reacs= [r.id for r in self.model.exchanges]
        return reacs

    def get_uptake_reactions(self):
        drains= self.model.exchanges
        reacs =[r.id for r in drains if r.reversibility or
                (r.lower_bound <0 and len(r.reactants)>0) or
                (r.upper_bound >0  and len(r.products) >0)]
        return reacs

    def get_internal_reactions(self):
        l1 = [r.id for r in self.model.reactions]
        l2 = [r.id for r in self.model.exchanges]
        reacs = set(l1) - set(l2)
        return list(reacs)

    def get_reactions_ids(self):
        reacs = [r.id for r in self.model.reactions]
        return reacs

    def get_bounds(self, rId):
        return self.model.reactions.get_by_id(rId).lower_bound, self.model.reactions.get_by_id(rId).upper_bound

    def get_constraints_reacs(self):
        return self.constraints.keys()

    def set_objective_function(self, objective):
        self.objective = objective

    def find_essential_proteins(self):
        proteins = self.model.proteins
        essential = []
        with self.model as m:
            if self.constraints:
                # apply the constraints of simulation problem
                for reac ,bounds in self.constraints.items():
                    m.reactions.get_by_id(reac).lower_bound = bounds[0]* GeckoConfigurations.SCALE_CONSTANT
                    m.reactions.get_by_id(reac).upper_bound = bounds[1]* GeckoConfigurations.SCALE_CONSTANT
            # for each protein check the essentially
            for p in proteins:
                r = m.reactions.get_by_id("draw_prot_" + p)
                lb = r.lower_bound
                ub = r.upper_bound
                r.lower_bound = 0
                r.upper_bound = 0
                res = m.optimize()
                r.lower_bound = lb
                r.upper_bound = ub
                if res.objective == 0:
                    essential.append(p)
        return essential

    def simulate(self, overrideSimulProblem=None):
        """
        This method preforms the phenotype simulation of the GeckoModel with the modifications present in the overrideSimulProblem.
        Args:
            overrideProblem (overrideStoicSimulProblem): override simulation Problem

        Returns:
            GeckoSimulationResult: Returns an object with the steady-state flux distribution, protein concentrations and solver status.
        """

        new_constraints = OrderedDict()
        if overrideSimulProblem is not None:
            new_constraints = overrideSimulProblem.get_modifications()

        if self.constraints is not None:
            new_constraints.update(self.constraints)

        with self.model:
            for rId in list(self.constraints.keys()):
                reac = self.model.reactions.get_by_id(rId)
                reac.bounds = (self.constraints.get(rId)[0] * GeckoConfigurations.SCALE_CONSTANT, self.constraints.get(rId)[1]* GeckoConfigurations.SCALE_CONSTANT)
            solution = self.model.optimize()
        # print("simulation time ", time)
        status = solverStatus.UNKNOWN

        if solution.status == "optimal":
            status = solverStatus.OPTIMAL

        fluxDist = solution.fluxes

        fluxes, prots = {},{}
        for k,v in fluxDist.items():
            if k.startswith("draw_prot_"):
                prots[k[10:]]= v / GeckoConfigurations.SCALE_CONSTANT
            else:
                fluxes[k] = v / GeckoConfigurations.SCALE_CONSTANT

        return GeckoSimulationResult(self.model.id, solverStatus=status, ssFluxesDistrib=fluxes,
                                          protConcentrations=prots, overrideSimulProblem=overrideSimulProblem)


class StoicSimulationProblem(SimulationProblem):
    """
        This class contains all required information to perform a simulation of a stoichiometric metabolic model.

    """

    def __init__(self, model, objective=None, minimize=False, constraints=None, solverId=StoicConfigurations.SOLVER,
                 method=StoicConfigurations.SOLVER_METHOD,  withCobraPy = False):
        """
        Create a StoicSimulationProblem instance.
        Args:
            model (CBModel): Stoichiometric metabolic model
            objective (dict): Objective coefficients (optional)
            minimize (bool): Minimize objective function (False by default)
            constraints (dict): Environmental conditions or additional constraints (optional)
            solverId (str): Solver id ("cplex" or "gurobi")
            method (str): Simulation method ("FBA", "pFBA", "MOMA", "lMOMA" and "ROOM")
            withCobraPy (bool): Solve the problem using CobraPy package (default false)
        """
        self.withCobraPy= withCobraPy
        if self.withCobraPy:
            if objective:
                model.objective = next(iter(objective.keys())) # only the first reac id will be set as objective function with coeficient 1
            # set the objective reaction in simulation problem obj
            (reac, coef)  = next(iter(linear_reaction_coefficients(model).items()))
            self.objective = {reac.id:coef}
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
            drains = self.model.exchanges
            reacs = [r.id for r in drains if r.reversibility or
                     (r.lower_bound < 0 and len(r.reactants) > 0) or
                     (r.upper_bound > 0 and len(r.products) > 0)]

        else:
            drains = list(self.model.get_exchange_reactions())

            reacs = [r for r in drains if self.model.reactions[r].reversible or
                     ((self.model.reactions[r].lb is None or self.model.reactions[r].lb<0 )and len(self.model.reactions[r].get_substrates())>0)or
                     ((self.model.reactions[r].ub is None or self.model.reactions[r].ub> 0 )and len(self.model.reactions[r].get_products()))>0]
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
            if (solution.values is None or any([solution.values[rId]==0 for rId in hasFlux])):
                essential.append(d)
            constraints[d] = (StoicConfigurations.DEFAULT_LB, StoicConfigurations.DEFAULT_UB)

        return essential




    def simulate(self, overrideSimulProblem=None):
        """
        This method preform the phenotype simulation of the stoichiometric model, using the solver method and applying
        the modifications present in the instance of overrideSimulProblem.

        Args:
            overrideProblem (OverrideStoicSimulProblem): Modification over the stoichiometric model and the default constraints.

        Returns:
            StoicSimulationResult: Returns an object with the steady-state flux distribution, solver status, etc..
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
    if method == 'FBA':
        solution = FBA(model, objective=objective, minimize=minimize, constraints=constraints)
    elif method == 'pFBA':
        solution = pFBA(model, objective=objective, minimize=minimize, constraints=constraints)
    # elif method == 'MOMA':
    #     solution = MOMA(mo
    # del, objective=objective, minimize=minimize, constraints=constraints, solver=solver)
    # elif method == 'lMOMA':
    #     solution = lMOMA(model, objective=objective, minimize=minimize, constraints=constraints, solver=solver)
    # elif method == 'ROOM':
    #     solution = ROOM(model, objective=objective, minimize=minimize, constraints=constraints, solver=solver)
    else:
        raise Exception(
            "Unknown method to perform the simulation.")
    return solution.status, solution.values


def _run_stoic_simutation_with_cobra(model, constraints):
    with model:
        for rId in list(constraints.keys()):
            reac = model.reactions.get_by_id(rId)
            reac.bounds=(constraints.get(rId)[0], constraints.get(rId)[1])
        solution = model.optimize()
    #print("simulation time ", time)
    status = solverStatus.UNKNOWN
    if solution.status == "optimal":
        status = solverStatus.OPTIMAL
    return status, solution.fluxes

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
        #if solver returns a solution where any concentration is negative
        for c  in X[1]:
            if c < -1*SolverConfigurations.RELATIVE_TOL:
                return solverStatus.ERROR, {}, {}

    except Exception:
        print("Error on solver!!!")
        # print X
        # print finalRates
        return solverStatus.ERROR,{}, {}

    #print(finalRates)
    # values bellow solver precision will be set to 0
    finalRates.update({k: 0 for k, v in finalRates.items() if
                       v < SolverConfigurations.ABSOLUTE_TOL and v > - SolverConfigurations.ABSOLUTE_TOL})
    conc = OrderedDict(zip(model.metabolites.keys(), X[1]))
    return solverStatus.OPTIMAL, finalRates, conc
