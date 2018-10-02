
def  generator_single_int_set(random, args):
    """
    Function to generate a new individual using the integer set representation.
    The function returns a set of integer values with a maximum of *candidate_max_size* elements.

    Args:
        random : the random number generator object
        args (dict) : a dictionary of keyword arguments

    Returns:
        set: a new individual

    Notes:
        Required  arguments in args:
        - *candidate_max_size* : number of integer values which compose a individual.
        - *_ec* : configuration of evolutionary computation. The argument bounder is required to get the maximum value allowed for the individual values.
    """
    size = random.randint(1, args["candidate_max_size"])
    bounder = args["_ec"].bounder
    representation = {random.randint(next(bounder.lower_bound), next(bounder.upper_bound)) for i in range(size)}
    return representation

def generator_single_int_tuple(random, args):
    """
    Function to generate a new individual using the integer tuple representation.
    The function returns a set of tuples values with a maximum of *candidate_max_size* elements.

    Args:
        random: the random number generator object
        args (dict): keyword arguments

    Returns:
        set: a new individual where each element is composed by a tuple.

    Notes:
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
        if id1 not in tuples.keys():
            tuples[id1] = id2
    return {(a, b) for a, b in tuples.items()}

def generator_tuple_int_set(random, args):
    """
    Function to generate a new individual using the integer representation.
    The function returns two integer sets.

    Args:
        random: the random number generator object
        args (dict): keyword arguments

    Returns:
        tuple : returns a tuple with two integer sets.

    """
    size1 = random.randint(1, args["candidate_max_size"][0])
    size2 = random.randint(1, args["candidate_max_size"][1])
    # first element of array has the lowers bounds and second element the upper bounds.
    bounder = args["_ec"].bounder
    set1 = {random.randint(bounder.lower_bound[0], bounder.upper_bound[0]) for i in range(size1)}
    set2 = {random.randint(bounder.lower_bound[1], bounder.upper_bound[1]) for i in range(size2)}
    #print (set1)
    #print (set2)
    #print ("--------")
    return (set1, set2)
