from anneal import *
from display import display_lines
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

def route_energy(state):
	"""Calculates the energy required to complete the route."""
	e = 0
	for i in range(len(state)):
            if(isinstance(state[0], HealthStation)):
                e += 1000
            e += distance( state[i-1], state[i] )
	return e

def start_simulation(cellList):
    """Recieves a cell list"""

    # Initial configuration (Random)
    state = cellList
    random.shuffle(state)

    annealer = Annealer(route_energy, route_move)
    state, e = annealer.anneal(state, 10000000, 0.01, 18000*len(state), 9)
    #state, e = annealer.anneal(state, 100, 0.01, 180*len(state), 10)
    
    x = distance(state[0], state[-1])

    print "%i mile route:" % (e-x)
    for cell in state:
            print "\t", cell
    return state


