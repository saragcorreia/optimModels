from collections import OrderedDict
from libsbml import readSBMLFromFile
from framed.io.sbml import _load_compartments, _load_metabolites, _load_reactions, _load_global_parameters, _load_local_parameters, _load_ratelaws, _load_assignment_rules, _load_concentrations, ODEModel
from math import log

def load_kinetic_model(filename):
    document = readSBMLFromFile(filename)
    sbml_model = document.getModel()

    if sbml_model is None:
        raise IOError('Failed to load model.')

    model = dynamicModel(sbml_model.getId())

    _load_compartments(sbml_model, model)
    _load_metabolites(sbml_model, model)
    _load_reactions(sbml_model, model)
    _load_concentrations(sbml_model, model)
    _load_global_parameters(sbml_model, model)
    _load_local_parameters(sbml_model, model)
    _load_ratelaws(sbml_model, model)
    _load_assignment_rules(sbml_model, model)

    return model



class dynamicModel(ODEModel):
    def __init__(self, model_id):
        """
        Arguments:
            model_id (str): a valid unique identifier
        """
        ODEModel.__init__(self, model_id)


    def build_ode(self):
        if not self._func_str:
            parsed_rates = {r_id: self.parse_rate(r_id, ratelaw)
                            for r_id, ratelaw in self.ratelaws.items()}

            parsed_rules = {p_id: self.parse_rule(rule, parsed_rates)
                            for p_id, rule in self.assignment_rules.items()}

            rate_exprs = ["    r['{}'] = factor['{}']*({})".format(r_id, r_id, parsed_rates[r_id])
                          for r_id in self.reactions]

            balances = [' ' * 8 + self.print_balance(m_id) for m_id in self.metabolites]
            # balances[54] = ' ' * 8 +  str(0)
            # balances[55] = ' ' * 8 + str(0)
            # balances[64] = ' ' * 8 + str(0)
            # balances[65] = ' ' * 8 + str(0)
            # balances[66] = ' ' * 8 + str(0)
            # balances[71] = ' ' * 8 + str(0)

            rule_exprs = ["    v['{}'] = {}".format(p_id, parsed_rules[p_id])
                          for p_id in self.assignment_rules]

            func_str = 'def ode_func(t, x, r, p, v, factor):\n\n' + \
                       '\n'.join(rule_exprs) + '\n\n' + \
                       '\n'.join(rate_exprs) + '\n\n' + \
                       '    dxdt = [\n' + \
                       ',\n'.join(balances) + '\n' + \
                       '    ]\n\n' + \
                       '    return dxdt\n'
                       #'    x = [max(val,1e-9) for val in x] \n\n' + \
                       #'    print dxdt\n' + \
                       #'    res = [a * -1.0 if abs(a + b) < 1e-9 else b for (a, b) in zip(x, dxdt)]\n\n'+ \
                       #'    print res\n' + \


            self._func_str = func_str
           # print self._func_str
        return self._func_str





    def get_ode(self, r_dict=None, params=None, factors= None):

        p = self.merge_constants()
        v = self.variable_params.copy()

        if r_dict is not None:
            r = r_dict
        else:
            r = {}

        if params:
            p.update(params)

        allFactors =  OrderedDict([(r_id, 1) for r_id in self.reactions])

        if factors:
            allFactors.update(factors)

        exec self.build_ode() in globals()

        ode_func = eval('ode_func')

        #print str(self.metabolites.keys())

        #print str(r)
        #print str(p)
        #print str(v)
        #print str(allFactors)
        #print str(ode_func)
        f = lambda t, x: ode_func(t, x, r, p, v, allFactors)
        return f


    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
