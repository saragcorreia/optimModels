import copy
from random import Random
from inspyred.ec.variators.crossovers import crossover
from inspyred.ec.variators.mutators import mutator


@mutator
def grow_mutation_intSetRep(random, candidate, args):
    #bounder = inspyred.ec.Bounder(0,10)
    bounder = args["_ec"].bounder
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate
    maxSize = args["candidate_max_size"]
    mutant = copy.copy(candidate)

    if len(mutant) < maxSize:
        newElem = random.randint(bounder.lower_bound.next(), bounder.upper_bound.next())
        while newElem in mutant:
            newElem = random.randint(bounder.lower_bound.next(), bounder.upper_bound.next())
        mutant.add(newElem)
    #print str(candidate)+"--grow->"+str(mutant)
    return mutant



@mutator
def shrink_mutation(random, candidate, args):
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate
    mutant = copy.copy(candidate)
    if len(mutant)>1:
        index = random.randint(0, len(mutant)-1)
        mutantL = list(candidate)
        mutantL.sort()
        mutantL.pop(index)
        mutant = set(mutantL)
    #print str(candidate)+"--shrink->"+str(mutant)
    return mutant

@mutator
def single_mutation_intSetRep(random, candidate, args):
    bounder = args["_ec"].bounder
    #bounder = inspyred.ec.Bounder(0,10)
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate
    mutant = copy.copy(candidate)
    index = random.randint(0, len(mutant)-1)
    newElem = random.randint(bounder.lower_bound.next(), bounder.upper_bound.next())
    while newElem in mutant:
        newElem = random.randint(bounder.lower_bound.next(), bounder.upper_bound.next())
    mutantL = list(mutant)
    mutantL[index]=newElem
    mutant= set(mutantL)
    #print str(candidate)+" --replace-> "+str(mutant)
    return mutant

@mutator
def grow_mutation_intTupleRep(random, candidate, args):
  bounder = args["_ec"].bounder
  mutRate = args.setdefault("mutation_rate", 0.1)
  #bounder = inspyred.ec.Bounder([0, 0], [47, 10])
  if random.random() > mutRate:
      return candidate
  maxSize = args["candidate_max_size"]
  mutant = copy.copy(candidate)

  if len(mutant) < maxSize:
      elem = _generate_new_tupple(random, mutant, bounder)
      mutant.add(elem)
  #print str(candidate)+"--grow->"+str(mutant)
  return mutant

@mutator
def single_mutation_intTupleRep(random, candidate, args):
    bounder = args["_ec"].bounder
    # bounder = inspyred.ec.Bounder([0,0],[47,10])
    mutRate = args.setdefault("mutation_rate", 0.1)
    if random.random() > mutRate:
        return candidate
    mutant = copy.copy(candidate)

    index = random.randint(0, len(mutant)-1)

    mutantL = list(mutant)
    mutantL[index] = _generate_new_tupple(random, mutant, bounder)
    mutant= set(mutantL)
   # print str(candidate)+" --replace-> "+str(mutant)
    return mutant

def _generate_new_tupple(random, mutant, bounder):
    reacsCandidate = {k for (k, v) in mutant}
    id1 = random.randint(bounder.lower_bound[0], bounder.upper_bound[0])
    id2 = random.randint(bounder.lower_bound[1], bounder.upper_bound[1])
    while id1 in reacsCandidate:
        id1 = random.randint(bounder.lower_bound[0], bounder.upper_bound[0])
    return (id1,id2)

@crossover
def uniform_crossover(random, mom, dad, args):
    crossRate = args.setdefault("crossover_rate", 1.0)
    children=[]
    if random.random() > crossRate or (len(mom)==1 and len(dad)==1):
        children.append(mom)
        children.append(dad)
        #print "crossover pass"
        return children

    maxSize = args["candidate_max_size"]
    intersection = mom & dad
    otherElems = list((mom | dad).difference(intersection))
    child1 = copy.copy(intersection)
    child2 = copy.copy(intersection)

    while len(otherElems)>0:
        prob =0.5
        elemPosition = random.randint(0, len(otherElems)-1)
        if len(child1) >=maxSize or len(child2)==0:
            prob = 0
        elif len(child2) >= maxSize or len(child1)==0:
            prob = 1

        r = random.random()
        if r <= prob:
            child1.add(otherElems[elemPosition])
        else:
            child2.add(otherElems[elemPosition])
        otherElems.pop(elemPosition)

    children.append(child1)
    children.append(child2)
    #print "cross over"
    #print str(mom) + " ; "+str(dad)
    #print str(child1) + " ; " + str(child2)
    return children




if __name__ == '__main__':
    candidate = [{1,2,3,6},{2,4,5},{1},{7,8}]
    candidate= [{(1,2),(22,3),(3,2)},{(2,4),(5,1)},{(1,1)},{(7,1),(8,1)}]
    print candidate


    args = {"candidate_max_size":5, "mutation_rate":1.0}
    rand = Random()
    print "----- grow mutation ------"
    grow_mutation_intTupleRep(rand, candidate, args)
    print "----- shrink mutation ------"
    shrink_mutation(rand, candidate, args)
    print "----- single muation ------"
    single_mutation_intTupleRep(rand, candidate, args)
    print "----- uniform crossover ------"
    uniform_crossover(rand, candidate, args)
