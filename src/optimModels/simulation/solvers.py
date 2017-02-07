import odespy

from src.optimModels import solverParameters, Parameter

class odeSolver:
    LSODA = 1
    LSODAR = 2
    LSODE = 3
    HEUN = 4
    EULER = 5
    RK4 =  6
    DORMAN_PRINCE = 7
    RKFehlberg = 8
    Dopri5 = 9
    Dop853 = 10
    Vode = 11
    Radau5 = 12
    AdamsBashforth2=13
    AdamsBashMoulton2=14

    def __init__(self, solverId):
        self.solverId = solverId

    def get_solver(self, odeProblem):
        if self.solverId is odeSolver.LSODA:
            solver = odespy.Lsoda(odeProblem.func)
        elif self.solverId is odeSolver.LSODAR:
            solver = odespy.Lsodar(odeProblem.func)
        elif self.solverId is odeSolver.LSODE:
            solver = odespy.Lsode(odeProblem.func)
        elif self.solverId is odeSolver.HEUN:
            solver = odespy.Heun(odeProblem.func)
        elif self.solverId is odeSolver.EULER:
            solver = odespy.Euler(odeProblem.func)
        elif self.solverId is odeSolver.RK4:
            solver = odespy.RK4(odeProblem.func)
        elif self.solverId is odeSolver.DORMAN_PRINCE:
            solver = odespy.DormandPrince(odeProblem.func)
        elif self.solverId is odeSolver.RKFehlberg:
            solver = odespy.RKFehlberg(odeProblem.func)
        elif self.solverId is odeSolver.Dopri5:
            solver = odespy.Dopri5(odeProblem.func)
        elif self.solverId is odeSolver.Dop853:
             solver = odespy.Dop853(odeProblem.func)
        elif self.solverId is odeSolver.Vode:
            solver = odespy.Vode(odeProblem.func)
        elif self.solverId is odeSolver.AdamsBashforth2:
            solver = odespy.AdamsBashforth2(odeProblem.func, method='bdf')
        elif self.solverId is odeSolver.Radau5:
            solver = odespy.Radau5(odeProblem.func)
        elif self.solverId is odeSolver.AdamsBashMoulton2:
            solver = odespy.AdamsBashMoulton2(odeProblem.func)
        elif self.solverId is 15:
            print odespy.list_available_solvers()
            solver = odespy.Lsoda(odeProblem.func,)

        # increase by default the number of steps for LSODA
        if self.solverId is odeSolver.LSODA or self.solverId is odeSolver.LSODAR:
            solver.nsteps = solverParameters[Parameter.N_STEPS]

        solver.atol = solverParameters[Parameter.ABSOLUTE_TOL]
        solver.rtol = solverParameters[Parameter.RELATIVE_TOL]

        return solver

