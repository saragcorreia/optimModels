from inspyred.ec import Individual


def new_candidates_replacement(random, population, parents, offspring, args):
    """Performs replacement for the offspring.

    This function performs a new candidates replacement, which means that
    the offspring replace the least fit individuals in the existing
    population, even if those offspring are less fit than the individuals
    that they replace. Moreover a new set of candidates random generated
    will be added to the population

    .. Arguments:
       random -- the random number generator object
       population -- the population of individuals
       parents -- the list of parent individuals
       offspring -- the list of offspring individuals
       args -- a dictionary of keyword arguments

    """
    population.sort()
   # print "population"
    num_to_replace = min(len(offspring), len(population))
    population[:num_to_replace] = offspring[:num_to_replace]
    population.sort()
    # generate new candidates
    numNewCandidates = int(round(args.setdefault("new_candidates_rate", 0.0) * len(population)))
    newCandidates = _generateNewCandidates(numNewCandidates, random, args)
    population[:len(newCandidates)] = newCandidates

    #print population
    #print len(population)
    #print " END population"
    return population


def new_candidates_no_duplicates_replacement(random, population, parents, offspring, args):
    """Performs replacement for the offspring.

    This function performs a new candidates replacement, which means that
    the offspring replace the least fit individuals in the existing
    population, even if those offspring are less fit than the individuals
    that they replace.Moreover a new set of candidates random generated
    will be added to the population. The duplicated candidates are
    replaced by new ones randomly generated.

    .. Arguments:
       random -- the random number generator object
       population -- the population of individuals
       parents -- the list of parent individuals
       offspring -- the list of offspring individuals
       args -- a dictionary of keyword arguments

    """

    population.sort()
   # print "--------- population replacement ---------------"
    num_to_replace = min(len(offspring), len(population))
    population[:num_to_replace] = offspring[:num_to_replace]
    population.sort()

    # generate new candidates
    numNewCandidates = int(round(args.setdefault("new_candidates_rate", 0.0) * len(population)))
    newCandidates = _generateNewCandidates(numNewCandidates, random, args)
    population[:len(newCandidates)] = newCandidates


    # remove duplicates
    newPopulation = []
    for elem in population:
        if  not _candidateInPopulation(elem.candidate , newPopulation):
            newPopulation.append(elem)

    #complete the population size with new elements
    numNewCandidates = len(population) - len(newPopulation)
   # print "number of duplicated elements to remove:" + str(numNewCandidates)
    newCandidates = _generateNewCandidates(numNewCandidates, random, args)
    newPopulation = newPopulation + newCandidates

    #print population
    #print len(population)
    #print " END population"
    return newPopulation

def _generateNewCandidates(numCandidates, random, args):
    newCandidates = []
    if numCandidates > 0:

        try:
            generator = args["_ec"].mp_generator
        except AttributeError:
            generator = args["_ec"].generator

        evaluator = args["_ec"].evaluator

        newElems = [generator(random=random, args=args) for i in range(numCandidates)]
        newFits = evaluator(candidates=newElems, args=args)

        for cs, fit in zip(newElems, newFits):
            if fit is not None:
                ind = Individual(cs, maximize=True) #SGC: REVER A PASSAGEM DESTE PARAMETRO maximize
                ind.fitness = fit
                newCandidates.append(ind)
    return newCandidates


def _candidateInPopulation(candidate, population):
    for ind in population:
        if ind.candidate == candidate:
            return True
    return False



