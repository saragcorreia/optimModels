===============
Getting started
===============

Default Configurations
-----------------------
The default configurations used in the optimization/simulation processes are in the optimModels.utils.configuration file.

Loading Kinetic models
-----------------------

*optimModels*, at the moment supports kinetic metabolic models. In the future, other kind of metabolic models, sucha as communities models and ME-models, will be supported by the package.
The process of loading a model is quite simple, and are based on the classes available on the *framed* package.

.. Despite the SBML file path which contains the metabolic model itself, the user must provide a dictionary with the information of the parameters (vMax or enzyme identifier) which will be used to perform the strain optimization.
.. If the *map* argument is not given, we assume that the vMax parameters associeted to each reaction has the follow identifier "vMax**<id of reaction>**".

We assume that the vMax parameters associeted to each reaction has the follow identifier "vMax**<id of reaction>**".

::

    from optimModels import load_kinetic_model
    model = load_kinetic_model('TinyModel_RHS.xml')

