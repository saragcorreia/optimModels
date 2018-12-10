====================
Phenotype Simulation
====================

Stoichiometric Simulation
--------------------------
The phenotype simulation of stoichiometric metabolic models are out of scope of this package.
For the phenotype prediction prupose, you can use the available methods on *framed* package,  developed by Daniel Machado.

For more information see:
GitHub: https://github.com/cdanielmachado/framed

GECKO Simulation
--------------------------
The phenotype simulation of GECKO metabolic models are out of scope of this package.
The GECKO toolbox contains a Python package(geckopy) for enhancing a Genome-scale model to account for Enzyme Constraints, using Kinetics and Omics. ics data.

For more information see:
GitHub:https://github.com/SysBioChalmers/GECKO

Kinetic Simulation
------------------
*optimModels* implements some basic support for working with kinetic models.

It now also supports models that contain assignment rules (see for example the
`Chassagnole 2002 <https://www.ebi.ac.uk/biomodels-main/BIOMD0000000051>`_ *E. coli* model).

Wild-type simulation
~~~~~~~~~~~~~~~~~~~~~~

Running a simple steady state simulation (uses odespy package, LSODA method):

::

    from optimModels import kinetic_simulation

    result = kinetic_simulation(model)

    result.print()

Simulation with diferent parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is possible override model parameters without changing the model:

::

    result = kinetic_simulation(model, parameters = {'Dil' : 0.2/3600})

    result.print()

Knockouts simulation
~~~~~~~~~~~~~~~~~~~~~

The simulation of reaction knockouts is done by multiplying vMax parameter with the factor 0,
for instance maxG6PDH = 0 will be knockout the reaction vG6PDH:
::

    result = kinetic_simulation(model, factors={'maxG6PDH': 0.0})

    result.print()

Under/Over expression simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simulation of under (over) expression enzymes is done by multiplying vMax parameter with the factor less than 1 (higher than 1)
::

    result = kinetic_simulation(model, factors={'maxG6PDH': 2.0})

    result.print()

