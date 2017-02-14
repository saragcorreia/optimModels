class modelType:
    STOICHIOMETRIC=0
    KINETIC=1


# class solverStatus:
#     """ Enumeration of possible solution status. """
#     OPTIMAL = 0
#     UNKNOWN = 1
#     ERROR = 2



class Parameter:
    """ Enumeration of parameters. """
    ABSOLUTE_TOL = 0
    RELATIVE_TOL = 1
    N_STEPS =2


solverParameters={Parameter.ABSOLUTE_TOL: 1e-9,
                  Parameter.RELATIVE_TOL: 1e-9,
                  Parameter.N_STEPS:100000}


def set_solver_parameter(parameter, value):
    """ Change the value for a given parameter (see list of supported parameters).
    Arguments:
        parameter (Parameter): parameter type
        value (float): parameter value
    """
    global solverParameters
    solverParameters[parameter] = value