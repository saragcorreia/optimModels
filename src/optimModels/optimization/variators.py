import copy
from inspyred.ec.variators.crossovers import crossover
from inspyred.ec.variators.mutators import mutator

#####################################################################
#   Operatores over integer set representation {id1, id2, ... ,id_n}
#####################################################################
@mutator
def grow_mutation_intSetRep(random, candidate, args):
    """Returns the mutant produced by a grow mutation on the candidate (when the representation is a set of integers).
    If a candidate solution has the maximum size candidate allowed, this function leaves it unchanged.

    Parameters
    ----------
    random  : the random number generator object
    candidate : the candidate solution
    args : a dictionary of keyword arguments

    Returns
    -------
    out : new candidate

    Optional keyword arguments in args:

    - *mutation_rate* -- the rate at which mutation is performed (default 0.1)
    """
    # bounder = inspyred.ec.Bounder(0,10)
    bounder = args["_ec"].bounder
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate
    maxSize = args["candidate_max_size"]
    mutant = copy.copy(candidate)

    if len(mutant) < maxSize:
        newElem = random.randint(next(bounder.lower_bound), next(bounder.upper_bound))
        while newElem in mutant:
            newElem = random.randint(next(bounder.lower_bound), next(bounder.upper_bound))
        mutant.add(newElem)
    # print str(candidate)+"--grow->"+str(mutant)
    return mutant


@mutator
def shrink_mutation(random, candidate, args):
    """Returns the mutant produced by shrink mutation on the candidate.
    If a candidate solution has length of 1, this function leaves it unchanged.

    Parameters
    ----------
    random  : the random number generator object
    candidate : the candidate solution
    args : a dictionary of keyword arguments

    Returns
    -------
    out : new candidate

    Optional keyword arguments in args:

    - *mutation_rate* -- the rate at which mutation is performed (default 0.1)
    """
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate or len(candidate) == 1:
        return candidate
    index = random.randint(0, len(candidate) - 1) if len(candidate)>1 else 0
    mutantL = list(candidate)
    del mutantL[index]
    mutant = set(mutantL)
    # print str(candidate)+"--shrink->"+str(mutant)
    return mutant


@mutator
def single_mutation_intSetRep(random, candidate, args):
    """Returns the mutant produced by a single mutation on the candidate (when the representation is a set of integers).
    The candidate size is maintained.

    Parameters
    ----------
    random  : the random number generator object
    candidate : the candidate solution
    args : a dictionary of keyword arguments

    Returns
    -------
    out : new candidate

    Optional keyword arguments in args:

    - *mutation_rate* -- the rate at which mutation is performed (default 0.1)
    """

    bounder = args["_ec"].bounder
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate

    mutant = copy.copy(candidate)
    index = random.randint(0, len(mutant) - 1) if len(mutant) > 1 else 0
    newElem = random.randint(next(bounder.lower_bound), next(bounder.upper_bound))
    while newElem in mutant:
        newElem = random.randint(next(bounder.lower_bound), next(bounder.upper_bound))
    mutantL = list(mutant)
    mutantL[index] = newElem
    mutant = set(mutantL)
    # print str(candidate)+" --replace-> "+str(mutant)
    return mutant

@crossover
def uniform_crossover(random, mom, dad, args):
    """Return the offspring of the uniform crossover on the candidate. Based on two candidates (parents) build 2 children:
    - elements present in both parents will be present in both children;
    - both children have at least one element;
    - elements present in only one parent have equal probability to be present in child 1 or child 2 (after each child has at least one element).


    Parameters
    ------------
    random : the random number generator object
    mom : the first parent candidate
    dad : the second parent candidate
    args : a dictionary of keyword arguments

    Optional keyword arguments in args:
    - *crossover_rate* -- the rate at which crossover is performed
      (default 1.0)
    """
    crossRate = args.setdefault("crossover_rate", 1.0)
    children = []
    if random.random() > crossRate or (len(mom) == 1 and len(dad) == 1):
        children.append(mom)
        children.append(dad)
        return children

    maxSize = args["candidate_max_size"]
    intersection = mom & dad
    otherElems = list((mom | dad).difference(intersection))
    child1 = copy.copy(intersection)
    child2 = copy.copy(intersection)

    while len(otherElems) > 0:
        elemPosition = random.randint(0, len(otherElems) - 1) if len(otherElems)>1 else 0
        if len(child1) == maxSize or len(child2) == 0:
            child2.add(otherElems[elemPosition])
        elif len(child2) == maxSize or len(child1) == 0:
            child1.add(otherElems[elemPosition])
        else:
            r = random.random()
            if r <= 0.5:
                child1.add(otherElems[elemPosition])
            else:
                child2.add(otherElems[elemPosition])

        otherElems.pop(elemPosition)

    children.append(child1)
    children.append(child2)
    # print ("cross over")
    # print (str(mom) + " ; "+str(dad))
    # print (str(child1) + " ; " + str(child2))
    return children


####################################################################################
#   Operatores over a set of tuples  {(id1, val1), (id2, val2), ....(id_, val_n), }
####################################################################################

@mutator
def grow_mutation_intTupleRep(random, candidate, args):
    """Returns the mutant produced by a grow mutation on the candidate (when the representation is a set of tuples).
    If a candidate solution has the maximum size candidate allowed, this function leaves it unchanged.

    Parameters
    ----------
    random  : the random number generator object
    candidate : the candidate solution
    args : a dictionary of keyword arguments

    Returns
    -------
    out : new candidate

    Optional keyword arguments in args:

    - *mutation_rate* -- the rate at which mutation is performed (default 0.1)
    """
    bounder = args["_ec"].bounder
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate

    maxSize = args["candidate_max_size"]
    mutant = copy.copy(candidate)

    if len(mutant) < maxSize:
        elem = _generate_new_tupple(random, mutant, bounder)
        mutant.add(elem)
    # print str(candidate)+"--grow->"+str(mutant)
    return mutant


@mutator
def single_mutation_intTupleRep(random, candidate, args):
    """Returns the mutant produced by a single mutation on the candidate (when the representation is a set of tuples).
    The candidate size is maintained.

    Parameters
    ----------
    random  : the random number generator object
    candidate : the candidate solution
    args : a dictionary of keyword arguments

    Returns
    -------
    out : new candidate

    Optional keyword arguments in args:

    - *mutation_rate* -- the rate at which mutation is performed (default 0.1)
    """
    bounder = args["_ec"].bounder
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate
    mutant = copy.copy(candidate)
    index = random.randint(0, len(mutant) - 1) if len(mutant)>1 else 0
    mutantL = list(mutant)
    mutantL[index] = _generate_new_tupple(random, mutant, bounder)
    mutant = set(mutantL)
    # print str(candidate)+" --replace-> "+str(mutant)
    return mutant


def _generate_new_tupple(random, mutant, bounder):
    reacsCandidate = {k for (k, v) in mutant}
    id1 = random.randint(bounder.lower_bound[0], bounder.upper_bound[0])
    id2 = random.randint(bounder.lower_bound[1], bounder.upper_bound[1])
    while id1 in reacsCandidate:
        id1 = random.randint(bounder.lower_bound[0], bounder.upper_bound[0])
    return (id1, id2)


@crossover
def uniform_crossover_intTupleRep(random, mom, dad, args):
    """Return the offspring of the uniform crossover on the candidate. Based on two candidates (parents) build 2 children:
    - elements present in both parents will be present in both children;
    - both children have at least one element;
    - elements present in only one parent have equal probability to be present in child 1 or child 2 (after each child has at least one element).


    Parameters
    ------------
    random : the random number generator object
    mom : the first parent candidate
    dad : the second parent candidate
    args : a dictionary of keyword arguments

    Optional keyword arguments in args:
    - *crossover_rate* -- the rate at which crossover is performed
      (default 1.0)
    """
    crossRate = args.setdefault("crossover_rate", 1.0)
    children = []
    if random.random() > crossRate or (len(mom) == 1 and len(dad) == 1):
        children.append(mom)
        children.append(dad)
        return children

    maxSize = args["candidate_max_size"]
    intersection = mom & dad
    otherElems = list((mom | dad).difference(intersection))
    child1 = copy.copy(intersection)
    child2 = copy.copy(intersection)

    #intersection keys
    #############################
    intkeys = {k for k,v in list(mom)}& {k for k,v in list(dad)}
    intkeys = intkeys.difference({k for k,v in list(intersection)})
    swap = bool(random.randint(0,1))
    for k in intkeys:
        v1 = [d2 for d1,d2 in dad if k==d1][0]
        v2 = [m2 for m1,m2 in mom if k==m1][0]
        if swap:
            child1.add((k, v2))
            child2.add((k, v1))
        else:
            child1.add((k,v1))
            child2.add((k, v2))
        swap = not swap
        otherElems.remove((k,v1))
        otherElems.remove((k,v2))
    #############################

    while len(otherElems) > 0:
        prob = 0.5
        elemPosition = random.randint(0, len(otherElems) - 1) if len(otherElems)>1 else 0
        if len(child1) >= maxSize or len(child2) == 0:
            prob = 0
        elif len(child2) >= maxSize or len(child1) == 0:
            prob = 1

        r = random.random()
        elem = otherElems[elemPosition]
        if r <= prob and elem[0] not in {k for (k,v) in child1}:
            child1.add(elem)
        elif elem[0] not in {k for (k,v) in child2}:
            child2.add(elem)
        else:
            child1.add(elem)
        otherElems.pop(elemPosition)

    children.append(child1)
    children.append(child2)
    # print ("cross over")
    # print (str(mom) + " ; "+str(dad))
    # print (str(child1) + " ; " + str(child2))
    return children



#####################################################################################################
#   Operatores over a tuple of integer set representation ({id1, id2,...id_n}, {id1, id2,..., id_n})
#####################################################################################################
@mutator
def grow_mutation_tuple_intSetRep(random, candidate, args):
    """Returns the mutant produced by a grow mutation on the candidate (when the representation is a set of integers).
    If a candidate solution has the maximum size candidate allowed, this function leaves it unchanged.

    Parameters
    ----------
    random  : the random number generator object
    candidate : the candidate solution
    args : a dictionary of keyword arguments

    Returns
    -------
    out : new candidate

    Optional keyword arguments in args:

    - *mutation_rate* -- the rate at which mutation is performed (default 0.1)
    """
    # bounder = inspyred.ec.Bounder(0,10)
    bounder = args["_ec"].bounder
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate
    maxSize = args["candidate_max_size"] # tuple with max length for each elem in tuple

    mutant = copy.copy(candidate)
    r = random.random()
    index = 0 if r<0.5 else 1 # choose if the mutation is done in the first or second int set.
    if len(mutant[index]) < maxSize[index]:
        newElem = random.randint(bounder.lower_bound[index], bounder.upper_bound[index])
        while newElem in mutant[index]:
            newElem = random.randint(bounder.lower_bound[index], bounder.upper_bound[index])
        mutant[index].add(newElem)
    # print str(candidate)+"--grow->"+str(mutant)
    return mutant


@mutator
def shrink_mutation_tuple(random, candidate, args):
    """Returns the mutant produced by shrink mutation on the candidate.
    If a candidate solution has length of 1, this function leaves it unchanged.

    Parameters
    ----------
    random  : the random number generator object
    candidate : the candidate solution
    args : a dictionary of keyword arguments

    Returns
    -------
    out : new candidate

    Optional keyword arguments in args:

    - *mutation_rate* -- the rate at which mutation is performed (default 0.1)
    """
    mutRate = args.setdefault("mutation_rate", 0.1)

    mutant = copy.copy(candidate)
    r = random.random()
    indexTuple = 0 if r<0.5 else 1 # choose if the mutation is done in the first or second int set.

    if random.random() > mutRate or len(candidate[indexTuple]) == 1:
        return candidate

    mutantL = list(candidate[indexTuple])
    index = random.randint(0, len(candidate[indexTuple]) - 1) if len(candidate[indexTuple])>1 else 0
    del mutantL[index]

    if indexTuple == 0:
        mutant = (set(mutantL), mutant[1])
    else:
        mutant = (mutant[0], set(mutantL))
    # print str(candidate)+"--shrink->"+str(mutant)
    return mutant


@mutator
def single_mutation_tuple_intSetRep(random, candidate, args):
    """Returns the mutant produced by a single mutation on the candidate (when the representation is a set of integers).
    The candidate size is maintained.

    Parameters
    ----------
    random  : the random number generator object
    candidate : the candidate solution
    args : a dictionary of keyword arguments

    Returns
    -------
    out : new candidate

    Optional keyword arguments in args:

    - *mutation_rate* -- the rate at which mutation is performed (default 0.1)
    """

    bounder = args["_ec"].bounder
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate
    mutant = copy.copy(candidate)
    r = random.random()
    indexTuple = 0 if r<0.5 else 1 # choose if the mutation is done in the first or second int set.

    index = random.randint(0, len(mutant[indexTuple]) - 1) if len(mutant[indexTuple])>1 else 0
    newElem = random.randint(bounder.lower_bound[indexTuple], bounder.upper_bound[indexTuple])
    while newElem in mutant[indexTuple]:
        newElem = random.randint(bounder.lower_bound[indexTuple], bounder.upper_bound[indexTuple])
    mutantL = list(mutant[indexTuple])
    mutantL[index] = newElem

    if indexTuple == 0:
        mutant = (set(mutantL), mutant[1])
    else:
        mutant = (mutant[0], set(mutantL))
    # print str(candidate)+" --replace-> "+str(mutant)
    return mutant

@crossover
def uniform_crossover_tuple(random, mom, dad, args):
    """Return the offspring of the uniform crossover on the candidate. Based on two candidates (parents) build 2 children:
    - elements present in both parents will be present in both children;
    - both children have at least one element;
    - elements present in only one parent have equal probability to be present in child 1 or child 2 (after each child has at least one element).


    Parameters
    ------------
    random : the random number generator object
    mom : the first parent candidate
    dad : the second parent candidate
    args : a dictionary of keyword arguments

    Optional keyword arguments in args:
    - *crossover_rate* -- the rate at which crossover is performed
      (default 1.0)
    """
    crossRate = args.setdefault("crossover_rate", 1.0)
    children = []
    r = random.random()
    indexTuple = 0 if r < 0.5 else 1  # choose if the mutation is done in the first or second int set.

    if random.random() > crossRate or (len(mom[indexTuple]) == 1 and len(dad[indexTuple]) == 1):
        children.append(mom)
        children.append(dad)
        return children

    maxSize = args["candidate_max_size"][indexTuple]
    r = random.random()
    indexTuple = 0 if r<0.5 else 1 # choose if the mutation is done in the first or second int set.

    p1 = mom[indexTuple]
    p2 = dad[indexTuple]

    intersection = p1 & p2
    otherElems = list((p1 | p2).difference(intersection))
    child1 = copy.copy(intersection)
    child2 = copy.copy(intersection)

    while len(otherElems) > 0:
        elemPosition = random.randint(0, len(otherElems) - 1) if len(otherElems) > 1 else 0
        if len(child1) == maxSize or len(child2) == 0:
            child2.add(otherElems[elemPosition])
        elif len(child2) == maxSize or len(child1) == 0:
            child1.add(otherElems[elemPosition])
        else:
            r = random.random()
            if r <= 0.5:
                child1.add(otherElems[elemPosition])
            else:
                child2.add(otherElems[elemPosition])

        otherElems.pop(elemPosition)

    if indexTuple==0:
        children.append((child1, mom[1]))
        children.append((child2, dad[1]))
    else:
        children.append((mom[0],child1))
        children.append((dad[0], child2))
    # print ("cross over")
    # print (str(mom) + " ; "+str(dad))
    # print (str(child1) + " ; " + str(child2))
    return children


if __name__ == '__main__':
    import random
    r = random.Random()
    uniform_crossover(r, {1,2},{3}, None)