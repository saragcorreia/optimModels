
from optimModels.simulation.run import steady_state_simulation
from optimModels.simulation.simulationResults import print_simul_result

from optimModels.model.kineticModel import load_kinetic_model


if __name__ == '__main__':
    #SBML_MODEL = "/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/TinyModel_RHS.xml"

    SBML_MODEL = '../../../examples/models/Millard2016v2.xml'
    #SBML_MODEL = '../../../examples/models/Jahan2016_chemostat_fixed.xml'
    #SBML_MODEL = '../../../examples/models/chassagnole2002.xml'
    #load Model
    model = load_kinetic_model(SBML_MODEL)

    # wild-type simulation
    result = steady_state_simulation(model)

    print_simul_result(result)

    # Change parameters
    # result = steady_state_simulation(model, parameters={'Dil': 0.2 / 3600})
    # print_simul_result(result)
    #
    # #Knockouts (the local parameters has the sufix of reactioId)
    # result = steady_state_simulation(model, factors={'vG6PDH_rmaxG6PDH': 0.0})
    # print_simul_result(result)
    #
    # # Under/over expression (the local parameters has the sufix of reactioId)
    # result = steady_state_simulation(model, factors={'vG6PDH_rmaxG6PDH': 2.0})
    # print_simul_result(result)
