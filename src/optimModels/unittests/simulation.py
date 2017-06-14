SBML_MODEL = '/Volumes/Data/Documents/Projects/DeCaF/Optimizations/Data/chassagnole2002.xml'

from optimModels.simulation.run import steady_state_simulation
from optimModels.model.kineticModel import load_kinetic_model


if __name__ == '__main__':
    #load Model
    model = load_kinetic_model(SBML_MODEL)

    # wild-type simulation
    result = steady_state_simulation(model)
    result.print_result()  # KO simulation

    # Change parameters
    result = steady_state_simulation(model, parameters={'Dil': 0.2 / 3600})
    result.print_result()

    #Knockouts
    result = steady_state_simulation(model, factors={'maxG6PDH': 0.0})
    result.print_result()

    # Under/over expression
    result = steady_state_simulation(model, factors={'maxG6PDH': 2.0})
    result.print_result()
