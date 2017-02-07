from collections import OrderedDict
from libsbml import readSBMLFromFile
from framed.io.sbml import _load_compartments, _load_metabolites, _load_reactions, _load_global_parameters, _load_local_parameters, _load_ratelaws, _load_assignment_rules, _load_concentrations, ODEModel


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

            rule_exprs = ["    v['{}'] = {}".format(p_id, parsed_rules[p_id])
                          for p_id in self.assignment_rules]

            func_str = 'def ode_func(t, x, r, p, v, factor):\n\n' + \
                       '\n'.join(rule_exprs) + '\n\n' + \
                       '\n'.join(rate_exprs) + '\n\n' + \
                       '    dxdt = [\n' + \
                       ',\n'.join(balances) + '\n' + \
                       '    ]\n\n' + \
                       '    return dxdt\n'

            self._func_str = func_str

        return self._func_str





    def get_ode(self, r_dict=None, params=None, newFactors= None):

        p = self.merge_constants()
        v = self.variable_params.copy()

        if r_dict is not None:
            r = r_dict
        else:
            r = {}

        if params:
            p.update(params)

        factor =  OrderedDict([(r_id, 1) for r_id in self.reactions])

        if newFactors:
            factor.update(newFactors)

        exec self.build_ode() in globals()
        ode_func = eval('ode_func')

        f = lambda t, x: ode_func(t, x, r, p, v, factor)
        return f
