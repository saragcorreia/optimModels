
def save_all_results(population, num_generations, num_evaluations, args):
    resultFile = args["results_file"]
    file = open(resultFile, 'a')
    #save the optimization configuration

    print "Number of generation:" + str(num_generations)
    config = args["configuration"]
    decoder = config.get_decoder()
    model = config.get_simulation_problem().model

    if num_generations == 0:
        file.write("population_size;candidate_max_size;crossover_rate; mutation_rate;new_candidates_rate; num_elites\n")
        file.write(config.get_parameters_str())
        file.write("Generation;Fitness;Candidate;Reactions \n")

    for ind in population:
        solution_decoded = decoder.candidate_decoded(ind.candidate, model)
        file.write(("{0};{1};{2};{3} \n").format(num_generations, ind.fitness, ind.candidate, solution_decoded))
    file.close()