====================
Phenotype Simulation
====================

*optimModels* implements some basic (and experimental) support for working with kinetic models.

It now also supports models that contain assignment rules (see for example the
`Chassagnole 2002 <https://www.ebi.ac.uk/biomodels-main/BIOMD0000000051>`_ *E. coli* model).

Stoichiometric Simulation
--------------------------
The phenotype simulation of stoichiometric metabolic models are out of scope of this package.
For the strain optimization prupose, you can use the available methods on *framed* package,  developed by Daniel Machado.

For more information see: http://framed.readthedocs.io/en/latest/

Kinetic Simulation
------------------

Wild-type simulation
~~~~~~~~~~~~~~~~~~~~~~

Running a simple steady state simulation (uses odespy package, LSODA method):

::

    from optimModels import steady_state_simulation, print_simul_result

    result = steady_state_simulation(model)

    print_simul_result(result)

Simulation with diferent parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is possible override model parameters without changing the model:

::

    result = steady_state_simulation(model, parameters = {'Dil' : 0.2/3600})

    print_simul_result(result)

Knockouts simulation
~~~~~~~~~~~~~~~~~~~~~

The simulation of reaction knockouts is done by multiplying vMax parameter with the factor 0,
for instance maxG6PDH = 0 will be knockout the reaction vG6PDH:
::

    result = steady_state_simulation(model, factors={'maxG6PDH': 0.0})

    print_simul_result(result)

Under/Over expression simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simulation of under (over) expression enzymes is done by multiplying vMax parameter with the factor less than 1 (higher than 1)
::

    result = steady_state_simulation(model, factors={'maxG6PDH': 2.0})

    print_simul_result(result)

