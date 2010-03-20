import random

def reproduction(virList):

    populationFitness=0
    averageFitness=0

    #calculate population fitness and average_fitness
    for virus in virList:
        populationFitness+=virus.fitness;
    averageFitness=float(populationFitness)/len(virList)

    print "popFit=%d | averageFit= %d\n" % (populationFitness,averageFitness)

    #calculate probability of being selected for reproduction
    pSelectList=[(virus,float(virus.fitness)/populationFitness) for virus in virList]

    print "selectedMembers: \n"+str([str(vir)+","+str(prob) for (vir,prob) in pSelectList])
    #select members of the population to reproduce
    selectedVirus=[]

    for i in xrange(len(virList)):
        selectionNumber=random.random()
        accumProb=0
        for (virus,probability) in pSelectList:
            accumProb+=probability
            if selectionNumber<=accumProb:
                selectedVirus.append(virus)
                break

    print "selectedMembers: \n"+str([str(vir) for vir in selectedVirus])


