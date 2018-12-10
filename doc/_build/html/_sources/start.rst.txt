===============
Getting started
===============

Default Configurations
-----------------------
*optimModels*, at the moment supports kinetic metabolic models, communities models and Gecko models.
The default configurations used in the optimization/simulation processes are in the optimModels.utils.configuration file.
The parameters of EA can be changed using the class optimModels.optimization.evolutionary_algorithm.EAConfigurations

Loading kinetic models
-----------------------
The process of loading a model is quite simple, and are based on the classes available on the *framed* package.

.. Despite the SBML file path which contains the metabolic model itself, the user must provide a dictionary with the information of the parameters (vMax or enzyme identifier) which will be used to perform the strain optimization.
.. If the *map* argument is not given, we assume that the vMax parameters associeted to each reaction has the follow identifier "vMax**<id of reaction>**".

We assume that the vMax parameters associated to each reaction has the follow identifier "vMax**<id of reaction>**".

::

    from optimModels import load_kinetic_model
    model = load_kinetic_model('TinyModel_RHS.xml')

Loading community models or stoichiometric models
-------------------------------------------------
::

    from framed.io.sbml import load_cbmodel
    model = load_cbmodel("Ec_iAF1260.xml", flavor="cobra")


Loading GECKO models
-----------------------
Please, to understand the GECKO models read the paper:

Sánchez, Benjamín J., et al. *"Improving the phenotype predictions of a yeast genome‐scale metabolic model by incorporating enzymatic constraints."*
Molecular systems biology 13.8 (2017): 935.

::

    from geckopy import GeckoModel
    model = GeckoModel("single-pool")
