====================
Phenotype Simulation
====================

*optimModels* implements some basic (and experimental) support for working with kinetic models.

It now also supports models that contain assignment rules (see for example the
`Chassagnole 2002 <https://www.ebi.ac.uk/biomodels-main/BIOMD0000000051>`_ *E. coli* model).

Stoichiometric Simulation
--------------------------
The phenotype simulation of stoichiometric metabolic models are out of scope of this package.
For the strain optimization prupose, we use the available methods on *framed* package,  developed by Daniel Machado.

For more information see: http://framed.readthedocs.io/en/latest/

Kinetic Simulation
------------------

Wild- type phenotype simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running a simple time-course simulation (uses scipy
`odeint <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html>`_):

::

    from framed import time_course
    T, X = time_course(model, time=100)


You can change the number of integration steps:

::

    time_course(model, time=100, steps=1000)

You can override model parameters without changing the model:

::

    time_course(model, time=100, parameters={'Vmax1': 10.0, 'Vmax2': 20.0})


Knockouts simulation
~~~~~~~~~~~~~~~~~~~~~

Find the steady-state metabolite concentrations and reaction rates:

::

    from framed import find_steady_state
    x_ss, v_ss = find_steady_state(model)

Again, you can easily override model parameters for simulation purposes:

::

    find_steady_state(model, parameters={'Vmax1': 10.0})


