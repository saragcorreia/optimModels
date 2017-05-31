import odespy

from optimModels.utils.constantes import solverParameters, Parameter, solverMethod


class odespySolver:
    """
    ODE solver method implemented on odespy package.
    """

    def __init__(self, solverMethod):
        self.solverMethod = solverMethod

    def get_solver(self, func):
        """
        Returns the solver method from odespy package.

        Parameters
        -----------
        func : function
            fucntion with ODE system.

        Returns
        ----------
            out : as instance of odeSolver.
        """
        if self.solverMethod is solverMethod.LSODA:
            solver = odespy.Lsoda(func)
        elif self.solverMethod is solverMethod.LSODAR:
            solver = odespy.Lsodar(func)
        elif self.solverMethod is solverMethod.LSODE:
            solver = odespy.Lsode(func)
        elif self.solverMethod is solverMethod.HEUN:
            solver = odespy.Heun(func)
        elif self.solverMethod is solverMethod.EULER:
            solver = odespy.Euler(func)
        elif self.solverMethod is solverMethod.RK4:
            solver = odespy.RK4(func)
        elif self.solverMethod is solverMethod.DORMAN_PRINCE:
            solver = odespy.DormandPrince(func)
        elif self.solverMethod is solverMethod.RKFehlberg:
            solver = odespy.RKFehlberg(func)
        elif self.solverMethod is solverMethod.Dopri5:
            solver = odespy.Dopri5(func)
        elif self.solverMethod is solverMethod.Dop853:
             solver = odespy.Dop853(func)
        elif self.solverMethod is solverMethod.Vode:
            solver = odespy.Vode(func)
        elif self.solverMethod is solverMethod.AdamsBashforth2:
            solver = odespy.AdamsBashforth2(func, method='bdf')
        elif self.solverMethod is solverMethod.Radau5:
            solver = odespy.Radau5(func)
        elif self.solverMethod is solverMethod.AdamsBashMoulton2:
            solver = odespy.AdamsBashMoulton2(func)

        # update default parameters
        solver.nsteps = solverParameters[Parameter.N_STEPS]
        solver.atol = solverParameters[Parameter.ABSOLUTE_TOL]
        solver.rtol = solverParameters[Parameter.RELATIVE_TOL]

        return solver

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


