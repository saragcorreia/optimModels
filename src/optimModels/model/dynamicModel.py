from collections import OrderedDict
from libsbml import readSBMLFromFile
from framed.io.sbml import _load_compartments, _load_metabolites, _load_reactions, _load_global_parameters, \
    _load_local_parameters, _load_ratelaws, _load_assignment_rules, _load_concentrations
from framed.model.odemodel import ODEModel
import re
from math import log
from  optimModels.utils.utils import MyTree


def load_kinetic_model(filename, map={}):
    """ Load a kinetic model SBML file.

        Parameters
        ----------
        filename : str
            Location of the SBML file.
        map : dictionary
            Dictionary with the parameters that can be used in the strain optmimization process for each reaction. {id_reaction: [param1, param2]}

        Returns
        -------
        dynamicModel
            contains all information related with the dynamic model (reactions, kinetic eqations, metabolites, compartments, etc.)
        out : dynamicModel
            Object of type 'dynamicModel'.

        Raises
        ------
        IOError
            When is not possible load the SBML file.

    """
    document = readSBMLFromFile(filename)
    sbmlModel = document.getModel()

    if sbmlModel is None:
        raise IOError('Failed to load model.')

    model = dynamicModel(sbmlModel.getId())

    _load_compartments(sbmlModel, model)
    _load_metabolites(sbmlModel, model)
    _load_reactions(sbmlModel, model)
    _load_concentrations(sbmlModel, model)
    _load_global_parameters(sbmlModel, model)
    _load_local_parameters(sbmlModel, model)
    _load_ratelaws(sbmlModel, model)
    _load_assignment_rules(sbmlModel, model)

    # parse rates, rules and xdot expressions
    model.set_reactions_parameters_association(map)
    model._set_parsed_attr()

    return model


class dynamicModel(ODEModel):
    """ Class to store information of dynamic models.
    This class is an extension of ODEModel class from FRAMED package. The methods  *build_ode* and *get_ode* are override to
    support the manipulations over the parameters or enzyme concentration level during the strain optimization process.
    The ode function returned by *get_ode* replace the negative concentration, received as argument, by 0 if the concentration is smaller than
    absolute tolerance or raise an exception if the concentration is significante negative value.

    """

    def __init__(self, modelId):
        """
        Create a instance of dynamicModel class.
         Parameters
         ----------
            modelId: str
            A valid unique identifier
        """
        ODEModel.__init__(self, modelId)
        self._reactionParamsAssociation = None;  # reaction->parameters association
        self._parsedRates = None;
        self._parsedRules = None;
        self._parsedXdot = None;

    def _set_parsed_attr(self):
        self._parsedRates = {rId: self.parse_rate(rId, ratelaw)
                             for rId, ratelaw in self.ratelaws.items()}

        aux = {pId: self.parse_rule(rule, self._parsedRates)
               for pId, rule in self.assignment_rules.items()}

        trees = [_build_tree_rules(vId, aux) for vId in aux.keys()]
        order = _get_oder_rules(trees)

        self._parsedRules = OrderedDict([(id, aux[id]) for id in order])

        self._parsedXdot = {mId: self.print_balance(mId) for mId in self.metabolites}

        print self._parsedRates
        print self._parsedRules
        print self._parsedXdot

    def build_ode(self, factors):
        """
            Build the ODE system.
            Parameters
            ----------
            factors : OrderedDict
                OrderedDict where the key is the parameter identifyer and the value is the level of change values
                between 0 and 1 represent a under expression, above 1 a over expression and 0 to represent the knockouts.

            Returns
            -------
            string
            out : string
                A string with the ode system.


        """

        # factors: ["vmax1": 0, "vmax2"=2, "ENZYME_ID":0]
        # divide vmax parameters from enzymes expression levels
        factorsEnz = OrderedDict([(k, v) for k, v in factors.items() if k in self.metabolites.keys()])
        factorsParam = OrderedDict([(k, v) for k, v in factors.items() if k not in factorsEnz.keys()])

        ruleExprs = ["    v['{}'] = {}".format(pId, self._parsedRules[pId])
                     for pId in self._parsedRules.keys()]

        rateExprs = []
        for rId in self.reactions.keys():
            newExp = self._parsedRates[rId]
            if rId in self._reactionParamsAssociation.keys():
                toModify = set(factorsParam.keys()).intersection(self._reactionParamsAssociation[rId])
                if len(toModify) > 0:
                    for elem in toModify:
                        newExp = re.sub(r"([pv]\['" + elem + "'\])", str(factorsParam[elem]) + r" * \1", newExp);
            rateExprs.append("    r['{}'] = {}".format(rId, newExp))

        balances = []
        for m_id in self.metabolites.keys():
            exp = self._parsedXdot[m_id]
            if m_id in factorsEnz.keys():
                if factors[m_id] == 0:
                    newExp = "0"
                else:
                    newExp = re.sub(r"\+\s*(\d)", r"+ \1 * " + str(factorsEnz[m_id]), exp);
                balances.append(' ' * 8 + newExp)
            else:
                balances.append(' ' * 8 + exp)

        func_str = 'def ode_func(t, x, r, p, v):\n\n' + \
                   '    newX = []\n' + \
                   '    for elem in x: \n' + \
                   '        if elem > -0.000001 and elem < 0: \n' + \
                   '            newX.append(0) \n' + \
                   '        elif  elem < 0: \n' + \
                   '            raise Exception\n' + \
                   '        else:  \n' + \
                   '            newX.append(elem) \n' + \
                   '    x = newX \n' + \
                   '\n'.join(ruleExprs) + '\n\n' + \
                   '\n'.join(rateExprs) + '\n\n' + \
                   '    dxdt = [\n' + \
                   ',\n'.join(balances) + '\n' + \
                   '    ]\n\n' + \
                   '    return dxdt\n'
        print func_str
        return func_str

    def get_ode(self, r_dict=None, params=None, factors=None):
        """
            Build the ODE system.
            Parameters
            ----------
            rDict: OrderedDict
                This variable is used to store the reaction rates.

            params: OrderedDict
                Parameters and the new values used to replace the original parameters present in the SBML model

            factors : OrderedDict
                OrderedDict where the key is the parameter identifyer and the value is the level of change values
                between 0 and 1 represent a under expression, above 1 a over expression and 0 to represent the knockouts.

            Returns
            -------
            function
            out : function
                A function used to solve the ODE system.


        """
        p = self.merge_constants()
        v = self.variable_params.copy()

        if r_dict is not None:
            r = r_dict
        else:
            r = {}

        if params:
            p.update(params)

        exec self.build_ode(factors) in globals()
        ode_func = eval('ode_func')

        f = lambda t, x: ode_func(t, x, r, p, v)
        return f

    def set_reactions_parameters_association(self, map):
        self._reactionParamsAssociation = map

    def get_reactions_parameters_association(self):
        self._reactionParamsAssociation = map

    def get_parameters_by_reaction(self, reactionId):
        res = []
        if reactionId in self._reactionParamsAssociation.keys():
            res = self._reactionParamsAssociation[reactionId]
        return res

    def get_reactions_by_parameter(self, paramId):
        res = []
        for r in self._reactionParamsAssociation.keys():
            if paramId in self._reactionParamsAssociation[r]:
                res = res + [r]
        return res

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


# auxiliar functions to set the assignment rules by the correct order in the ODE system
def _build_tree_rules(parent, rules):
    regexp = "v\[\'(.*?)\'\]"
    children = re.findall(regexp, rules[parent])
    if len(children) == 0:
        return MyTree(parent, None)
    else:
        childrenTrees = [_build_tree_rules(child, rules) for child in children]
        return MyTree(parent, childrenTrees)


def _get_oder_rules(trees):
    res = []
    for tree in trees:
        new_elems = _get_order_nodes(tree)
        [res.append(item) for item in new_elems if item not in res]
    print res
    return res


def _get_order_nodes(tree):
    res = [tree.name]
    if len(tree.children) > 0:
        for child in tree.children:
            res = _get_order_nodes(child) + res
    return res
