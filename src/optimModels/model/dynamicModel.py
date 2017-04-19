from collections import OrderedDict
from libsbml import readSBMLFromFile
from framed.io.sbml import _load_compartments, _load_metabolites, _load_reactions, _load_global_parameters, _load_local_parameters, _load_ratelaws, _load_assignment_rules, _load_concentrations
from framed.model.odemodel import ODEModel
import re
from  optimModels.utils.utils import MyTree

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

    def parse_rule(self, rule, parsed_rates):

        symbols = '()+*-/,'
        rule = ' ' + rule + ' '
        for symbol in symbols:
            rule = rule.replace(symbol, ' ' + symbol + ' ')

        for i, m_id in enumerate(self.metabolites):
            rule = rule.replace(' ' + m_id + ' ', ' x[{}] '.format(i))

        for c_id in self.compartments:
            rule = rule.replace(' ' + c_id + ' ', " p['{}'] ".format(c_id))

        for p_id in self.constant_params:
            rule = rule.replace(' ' + p_id + ' ', " p['{}'] ".format(p_id))

        for p_id in self.variable_params:
            rule = rule.replace(' ' + p_id + ' ', " v['{}'] ".format(p_id))
        import re
        for r_id in self.reactions:
            nrid = re.sub('\_medium$', '' ,r_id)
            rule = rule.replace(' ' + r_id + ' ', "(factor['{}']*({}))".format(nrid, parsed_rates[r_id]))
            #rule = rule.replace(' ' + r_id + ' ', "(factor['{}']*({}))".format(r_id, parsed_rates[r_id]))
            #rule = rule.replace(' ' + r_id + ' ', "r['{}']".format(r_id))

        return rule

    def build_ode(self):
        if not self._func_str:
            parsed_rates = {r_id: self.parse_rate(r_id, ratelaw)
                            for r_id, ratelaw in self.ratelaws.items()}

            parsed_rules = {p_id: self.parse_rule(rule, parsed_rates)
                            for p_id, rule in self.assignment_rules.items()}

            rate_exprs = ["    r['{}'] = factor['{}']*({})".format(r_id,re.sub('\_medium$', '' ,r_id), parsed_rates[r_id])
                          for r_id in self.reactions]

            # rate_exprs = ["    r['{}'] = factor['{}']*({})".format(r_id, r_id, parsed_rates[r_id])
            #               for r_id in self.reactions]
            balances = [' ' * 8 + self.print_balance(m_id) for m_id in self.metabolites]

            trees = [build_tree_rules(v_id, parsed_rules) for v_id in parsed_rules.keys()]
            order = get_oder_rules(trees)

            rule_exprs = ["    v['{}'] = {}".format(p_id, parsed_rules[p_id])
                          for p_id in order]

            func_str = 'def ode_func(t, x, r, p, v, factor):\n\n' + \
                       '\n'.join(rule_exprs) + '\n\n' + \
                       '\n'.join(rate_exprs) + '\n\n' + \
                       '    dxdt = [\n' + \
                       ',\n'.join(balances) + '\n' + \
                       '    ]\n\n' + \
                       '    return dxdt\n'

            self._func_str = func_str
            print self._func_str
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

        allFactors = OrderedDict([( r_id, 1) for r_id in self.reactions])

        if factors:
            allFactors.update(factors)

        exec self.build_ode() in globals()

        ode_func = eval('ode_func')

        #print str(self.metabolites.keys())
        #print "------------- // ______________-"
        #print  str(len(r)) + " --> "+ str(r)
        #print str(len(p)) + " --> "+ str(p)
        #print str(len(v)) + " --> "+ str(v)


        f = lambda t, x: ode_func(t, x, r, p, v, allFactors)
        return f


    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


# auxiliar functions to build the assignment rules by correct order
def build_tree_rules(parent, rules):
    regexp = "v\[\'(.*?)\'\]"
    children = re.findall(regexp,rules[parent])
    if len(children) == 0:
        return MyTree(parent, None)
    else:
        childrenTrees = [build_tree_rules(child, rules) for child in children]
        return MyTree(parent, childrenTrees)


def get_oder_rules(trees):
    res = []
    for tree in trees:
        new_elems = get_order_nodes(tree)
        [res.append(item) for item in new_elems if item not in res]
    print res
    return res

def get_order_nodes(tree):
    res = [tree.name]
    if len(tree.children) >0:
        for child in tree.children:
            res = get_order_nodes(child) + res
    return res