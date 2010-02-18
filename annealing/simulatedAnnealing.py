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
        dist=0
        salud = virus[0].hp

        if(isinstance(state[0], HealthStation)):
            e += 1000

	for i in range(len(state)):
            dist = distance( state[i-1], state[i])
            salud-=dist
            e+=dist
            if(salud < 0):
                e += 10000
            else:
                if i < len(state)-1 and isinstance(state[i+1],HealthStation):
                    if(salud>0):
                        e+=abs(salud-state[i+1].healRatio)

                        salud+=state[i+1].healRatio
                        dif=0
                        if salud>virus[0].maxHp:
                            dif=salud-virus[0].maxHp
                            salud=virus[0].maxHp
                        e-=state[i+1].healRatio+dif
	return e


def start_simulation(lienzo, virus):
    """Recieves a cell list"""

    # Initial configuration (Random)
    state = lienzo.annealedCells
    random.shuffle(state)

    tMax=1000
    tMin=0.001
    steps=1800*len(state)
    updates=10
    
    annealer = Annealer(route_energy, route_move,state, tMax, tMin, steps,lienzo,virus,updates)
    annealer.start()
    #state, e = annealer.anneal(state, 10000000, 0.01, 18000*len(state), 9)
    #state, e = annealer.anneal(state, 100, 0.01, 180*len(state), 10)
    #print "%i mile route:" % e
    for cell in state:
            print "\t", cell
    return state


