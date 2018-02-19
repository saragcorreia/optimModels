class optimType:
    REACTION_KO = 1
    REACTION_UO = 2
    GENE_KO = 3
    GENE_UO = 4
    MEDIUM = 5
    MEDIUM_LEVELS = 6
    MEDIUM_REACTION_KO = 7
    MEDIUM_REACTION_UO = 8
    COMPOSITION = 9


    types = {1:"Reaction Knockouts",2:"Reaction Under/Over expression", 3:"Gene Knockouts",
             4:"Gene Under/Over expression", 5:"Medium compositions",6:"Medium compositions with levels",
             7:"Medium with Reaction Knockouts",8: "Medium with Reaction Under/Over expression",
             9:"Community Composition"}

    def get_optim_type_name(self, id):
        return optimType.types.get(id)


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
    OPTIMAL = 1
    UNKNOWN = 0
    ERROR = 2
    SUBOPTIMAL = -1
    UNBOUNDED = -2
    INFEASIBLE = -3
    INF_OR_UNB = -4


    @staticmethod
    def get_status_str(id):
        if solverStatus.ERROR == id :
            str="Error"
        elif solverStatus.OPTIMAL == id:
            str = "Optimal"
        elif solverStatus.SUBOPTIMAL == id:
            str = "Sub-Optimal"
        elif solverStatus.UNBOUNDED == id or  solverStatus.INFEASIBLE == id or solverStatus.INF_OR_UNB == id:
            str = "Infeasible or unbounded problem."
        else:
            str = "Unknown"
        return str

