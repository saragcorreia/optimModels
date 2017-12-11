from optimModels.utils.configurations import EAConfigurations

def load_population (initPopFile = None, decoder = None):
    population = []
    if initPopFile is not None:

        with open(initPopFile, 'r') as file:
            data = file.readlines()

        for line in data:
             fields = line.split(';')
             num_generations = int(fields[0]) + 1
             candidateIds = eval(fields[3])
             candidate = set(decoder.candidate_decoded_ids_to_index(candidateIds))
             population.append(candidate)
        file.close()
    return num_generations, population





def save_all_results(population, num_generations, num_evaluations, args):
    """
    Print the output of the evolutionary computation to a file with the follow fields:
    - number of generation
    - fitness of candidate
    - the solution candidates
    - the solution encoded candidates

    Parameters
    -----------
    population : the population of Individuals
    num_generations : the number of elapsed generations
    num_evaluations : the number of evaluations already performed
    args : a dictionary of keyword arguments

    Optional keyword arguments in args:

    - *results_file* -- the file path of the result file
    - *configuration* -- the configuration of the EA algorithm

    """
    resultFile = args["results_file"]
    file = open(resultFile, 'a')

    print ("Number of generation:" + str(num_generations))
    config = args["configuration"]
    decoder = config.get_decoder()

    # save the optimization configuration
    if num_generations == 0:
        file.write("population_size;candidate_max_size;crossover_rate; mutation_rate;new_candidates_rate; num_elites\n")
        file.write(";".join(map(str,EAConfigurations.get_default_config())))
        file.write("Generation;Fitness;Candidate;Reactions\n")

    # save all candidates of the population
    for ind in population:
        solution_decoded = decoder.candidate_decoded(ind.candidate)
        file.write(("{0};{1};{2};{3} \n").format(num_generations, ind.fitness, ind.candidate, solution_decoded))
    file.close()

