=====================
Strain optimization
=====================

Kinetic models optimization
----------------------------

*optimModels* implements some basic (and experimental) support for working with strain optimization using Kinetic
metabolic models.

The optimization use several parameters which are configured in the optimModels.utils.configurations module.

Objective Function
~~~~~~~~~~~~~~~~~~~
Before start the strain optimization, it is required the definition of an objective function.
The objective function is responsible for calculate the fitness value for each candidate solution obtained during the
optimization process.

At the moment there are two objective functions available:
- *targetFlux* : the fitness value is the flux of a given target reaction.
- *BPCY* : the fitness value is the Biomass-Product Coupled Yield. In this case the user must
specify 3 reactions identifiers (biomass, product and uptake).

::

    from optimModels import build_objective_function

    objFunc = build_objective_function("targetFlux", ["vsersynth"])

Knockouts
~~~~~~~~~~~
The strain optimization using the knockouts can be performed calling the *strain_optim* function.

::

    from optimModels import strain_optim

    result = strain_optim(model, objFunc=objFunc)
    for r in result:
        print_simul_result(result)

Under/Over expression
~~~~~~~~~~~~~~~~~~~~~~
To performe a under/over expression optimization the multiplied factors levels should be given as argument.

::

    levels = [0, 2 ** -5, 2 ** -4, 2 ** -3, 2 ** -2, 2 ** -1, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]

    result = strain_optim(model, objFunc=objFunc, levels = levels)
    for r in result:
        print_simul_result(result)
