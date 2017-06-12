def  generator_intSetRep(random, args):
    """
    Function to generate a new individual using the integer set representation.
    The function returns a set of integer values with a maximum of *candidate_max_size* elements.

    Parameters
    ------------
    random : the random number generator object
    args : a dictionary of keyword arguments

    Returns
    --------
    out: a new individual

    Required  arguments in args:
    - *candidate_max_size* : number of integer values which compose a individual.
    - *_ec* : configuration of evolutionary computation. The argument bounder is required to get the maximum value allowed for the individual values.
    """
    size = random.randint(1, args["candidate_max_size"])
    bounder = args["_ec"].bounder
    representation = {random.randint(bounder.lower_bound.next(), bounder.upper_bound.next()) for i in range(size)}
    return representation

def generator_intTupleRep(random, args):
    """
    Function to generate a new individual using the integer tuple representation.
    The function returns a set of tuples values with a maximum of *candidate_max_size* elements.

    Parameters
    ------------
    random : the random number generator object
    args : a dictionary of keyword arguments

    Returns
    --------
    out: a new individual

    Required  arguments in args:
    - *candidate_max_size* : number of integer values which compose a individual.
    - *_ec* : configuration of evolutionary computation. The argument bounder is required to get the maximum value allowed for the individual values.
    """
    size = random.randint(1, args["candidate_max_size"])
    # first element of array has the lowers bounds and second element the upper bounds.
    bounder = args["_ec"].bounder
    tuples={}
    for i in range(size):
        id1 = random.randint(bounder.lower_bound[0], bounder.upper_bound[0])
        id2 = random.randint(bounder.lower_bound[1], bounder.upper_bound[1])
        if id1 not in tuples:
            tuples[id1] = id2
    return {(a, b) for a, b in tuples.iteritems()}
