# Optimization Models Framework
The Python framework under development will allow the strain design of single and microbial community cultures.
This documents presents a brief description of the framework and the main options taken during the development.

##Packages
 The framework python files are divided in four main packages:

###model:
This package contains functions to load and manipulate metabolic models. The loading of dynamic models (from SBML files) is based on the methods and classes present in the FRAMED framework ().

###simulation:
This package contains the classes and functions used to simulate different types of metabolic models (Kinetic, stoichiometric, … ) considering different phenotypes. For the dynamic models simulation, we use the Odespy framework, which offers a unified interface to a large collection of software for solving systems of ordinary differential equations (ODEs).

###optimization:
Contains all required entities to perform the optimization using evolutionary computation. The inspyred framework is used for creating biologically-inspired computational intelligence algorithms in Python, including evolutionary computation.

###utils:
Contains a set of generic and auxiliary functions, constants and configurations used by the methods developed in the framework.
