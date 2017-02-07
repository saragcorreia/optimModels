
"""
    ===============================================================
    :mod:`generators` -- generate solution for the optimization
    problem
    ===============================================================
    .. module:: evaluators
    .. moduleauthor:: Sara Correia <sarag.correia@gmail.com>
"""


# generate the indidual of a population where the max size, max index reaction and number of expression
# levels are passed as argument
def  generator_intSetRep(random, args):
    size = random.randint(1, args["candidate_max_size"])
    bounder = args["_ec"].bounder
    representation = {random.randint(bounder.lower_bound.next(), bounder.upper_bound.next()) for i in range(size)}
    return representation

def generator_intTupleRep(random, args):
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
