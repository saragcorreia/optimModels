
def load_population (initPopFile = None, decoder = None):
    """

    Args:
        initPopFile (str): file name with the population to be loaded.
        decoder (Decoder): decoder to decode the candidates.

    Returns:
        num_generations(str): number of the generation
        population (list): list of candidates
        fitness (list): fitness values for each candidate
    """
    population = []
    fitness = []
    if initPopFile is not None:

        with open(initPopFile, 'r') as file:
            data = file.readlines()

        for line in data:
             fields = line.split(';')
             num_generations = int(fields[0]) + 1
             fitness.append(fields[1])
             candidateIds = eval(fields[3])
             candidate = set(decoder.decode_candidate_ids_to_index(candidateIds))
             population.append(candidate)
        file.close()
    return num_generations, population, fitness

def save_all_results(population, num_generations, num_evaluations, args):
    """
    Print the output of the evolutionary computation to a file with the follow fields:
    - number of generation
    - fitness of candidate
    - the solution candidates
    - the solution encoded candidates

    Args:
        population (list): the population of Individuals
        num_generations (int): the number of elapsed generations
        num_evaluations (int): the number of evaluations already performed
        args (dict): a dictionary of keyword arguments

    Notes:
        Optional keyword arguments in args:
        - *results_file* -- the file path of the result file
        - *configuration* -- the configuration of the EA algorithm

    """
    print ("save results of generation:" + str(num_generations))
    resultFile = args["results_file"]
    file = open(resultFile, 'a')

    config = args["configuration"]
    decoder = config.get_decoder()

    # save the optimization configuration
    if num_generations == 0:
        file.write("population_size;candidate_max_size;crossover_rate; mutation_rate;new_candidates_rate; num_elites\n")
        file.write(";".join(map(str,config.get_ea_configurations().get_default_config())))
        file.write("Generation;Fitness;Candidate;Reactions\n")

    # save all candidates of the population
    for ind in population:
        solution_decoded = decoder.decode_candidate(ind.candidate)
        file.write(("{0};{1};{2};{3} \n").format(num_generations, ind.fitness, ind.candidate, solution_decoded))
    file.close()

