from anneal import *
#from healthStation import healRatio
from math import pow, sqrt
from healthStation import HealthStation
from display import *

def distance(a, b):
    return sqrt(pow(a.posX - b.posX,2) + pow(a.posY - b.posY,2))

def route_move(state):
	"""Swaps two cities in the route."""
	a = random.randint( 0, len(state)-1 )
	b = random.randint( 0, len(state)-1 )
	state[a], state[b] = state[b], state[a]

def route_energy(state, virus):
	"""Calculates the energy required to complete the route."""
	e = 0
        sumDistancia = 0
        salud = virus[0].hp
        if(isinstance(state[0], HealthStation)):
                e += 1000

	for i in range(len(state)):
            dist = distance( state[i-1], state[i] )
            e +=  dist
            #if(state)


        #for i in range(len(state)):


        #for i in range(len(state)):
            #sumDistancia +=  e
	return e

def start_simulation(lienzo, virus):
    """Recieves a cell list"""

    # Initial configuration (Random)
    state = lienzo.annealedCells
    random.shuffle(state)

    tMax=100
    tMin=0.001
    steps=180*len(state)
    updates=10
    
    annealer = Annealer(route_energy, route_move,state, tMax, tMin, steps,lienzo,virus,updates)
    annealer.start()
    #state, e = annealer.anneal(state, 10000000, 0.01, 18000*len(state), 9)
    #state, e = annealer.anneal(state, 100, 0.01, 180*len(state), 10)
    #print "%i mile route:" % e
    for cell in state:
            print "\t", cell
    return state


