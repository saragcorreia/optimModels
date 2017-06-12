class solverMethod:
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

    methods ={1:"LSODA",2:"LSODAR", 3: "LSODE", 4: "HEUN", 5: "EULER",
                6: "Range Kutta 4", 7: "DORMAN PRINCE", 8: "RKFehlberg", 9: "Dopri5", 10: "Dop853", 11: "Vode",
                12: "Radau5", 13: "AdamsBashforth2", 14: "AdamsBashMoulton2"
              }

    def get_solver_method_name(self, id):
        return solverMethod.methods.get(id)

class solverStatus:
    """ Enumeration of possible solution status. """
    OPTIMAL = 0
    UNKNOWN = 1
    ERROR = 2

    @staticmethod
    def get_status_str(id):
        if solverStatus.ERROR == id :
            str="Error"
        elif solverStatus.OPTIMAL == id:
            str = "Optimal"
        else:
            str = "Unknown"
        return str

class Parameter:
    """ Enumeration of parameters. """
    ABSOLUTE_TOL = 0
    RELATIVE_TOL = 1
    N_STEPS =2

solverParameters={Parameter.ABSOLUTE_TOL: 1e-9,
                  Parameter.RELATIVE_TOL: 1e-6,
                  Parameter.N_STEPS:10000}


def set_solver_parameter(parameter, value):
    """ Change the value for a given parameter (see list of supported parameters).
    Parameters
    -----------
    parameter : parameter type
    value : parameter value
    """
    global solverParameters
    solverParameters[parameter] = value