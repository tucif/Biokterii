#########################################################################
# Python module for simulated annealing - anneal.py - v1.0 - 2 Sep 2009
# 
# Copyright (c) 2009, Richard J. Wagner <wagnerr@umich.edu>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
##########################################################################
"""
This module performs simulated annealing to find a state of a system that
minimizes its energy.
"""

import copy
import math
import random
import sys
import time
from threading import Thread

def round_figures(x, n):
	"""Returns x rounded to n significant figures."""
	return round(x, int(n - math.ceil(math.log10(abs(x)))))

def time_string(seconds):
	"""Returns time in seconds as a string formatted HHHH:MM:SS."""
	s = int(round(seconds))  # round to nearest second
	h, s = divmod(s, 3600)   # get hours and remainder
	m, s = divmod(s, 60)     # split remainder into minutes and seconds
	return '%4i:%02i:%02i' % (h, m, s)

class Annealer(Thread):
	"""Performs simulated annealing by calling functions to calculate
	energy and make moves on a state.  The temperature schedule for
	annealing may be provided manually or estimated automatically.
	"""
	def __init__(self, energy, move,state,Tmax, Tmin, steps, lienzo,updates=0):
		self.energy = energy  # function to calculate energy of a state
		self.move = move      # function to make a random change to a state
                self.state=state
                self.Tmax=Tmax
                self.Tmin=Tmin
                self.steps=steps
                self.updates=updates
                self.lienzo=lienzo
                Thread.__init__( self )
        def run(self):
            self.anneal(self.state,self.Tmax,self.Tmin,self.steps,self.updates)

        def anneal(self, state, Tmax, Tmin, steps, updates=0):
		"""Minimizes the energy of a system by simulated annealing.
		
		Keyword arguments:
		state -- an initial arrangement of the system
		Tmax -- maximum temperature (in units of energy)
		Tmin -- minimum temperature (must be greater than zero)
		steps -- the number of steps requested
		updates -- the number of updates to print during annealing
		
		Returns the best state and energy found."""
		
		step = 0
		start = time.time()
		
		def update(T, E, acceptance, improvement):
			"""Prints the current temperature, energy, acceptance rate,
			improvement rate, elapsed time, and remaining time.
			
			The acceptance rate indicates the percentage of moves since the last
			update that were accepted by the Metropolis algorithm.  It includes
			moves that decreased the energy, moves that left the energy
			unchanged, and moves that increased the energy yet were reached by
			thermal excitation.
			
			The improvement rate indicates the percentage of moves since the
			last update that strictly decreased the energy.  At high
			temperatures it will include both moves that improved the overall
			state and moves that simply undid previously accepted moves that
			increased the energy by thermal excititation.  At low temperatures
			it will tend toward zero as the moves that can decrease the energy
			are exhausted and moves that would increase the energy are no longer
			thermally accessible."""
			
			elapsed = time.time() - start
			if step == 0:
				print ' Temperature        Energy    Accept   Improve     Elapsed   Remaining'
				print '%12.2f  %12.2f                      %s            ' % \
					(T, E, time_string(elapsed) )
			else:
				remain = ( steps - step ) * ( elapsed / step )
				print '%12.2f  %12.2f  %7.2f%%  %7.2f%%  %s  %s' % \
					(T, E, 100.0*acceptance, 100.0*improvement,
						time_string(elapsed), time_string(remain))
		
		# Precompute factor for exponential cooling from Tmax to Tmin
		if Tmin <= 0.0:
			print 'Exponential cooling requires a minimum temperature greater than zero.'
			sys.exit()
		Tfactor = -math.log( float(Tmax) / Tmin )
		
		# Note initial state
		T = Tmax
		E = self.energy(state)
		prevState = copy.deepcopy(state)
		prevEnergy = E
		bestState = copy.deepcopy(state)
		bestEnergy = E
		trials, accepts, improves = 0, 0, 0
		if updates > 0:
			updateWavelength = float(steps) / updates
			update(T, E, None, None)
		
		# Attempt moves to new states
		while step < steps:
                    self.lienzo.annealedCells=bestState
                    step += 1
                    T = Tmax * math.exp( Tfactor * step / steps )
                    self.move(state)
                    E = self.energy(state)
                    dE = E - prevEnergy
                    trials += 1
                    if dE > 0.0 and math.exp(-dE/T) < random.random():
                            # Restore previous state
                            state = copy.deepcopy(prevState)
                            E = prevEnergy
                    else:
                            # Accept new state and compare to best state
                            accepts += 1
                            if dE < 0.0:
                                    improves += 1
                            prevState = copy.deepcopy(state)
                            prevEnergy = E
                            if E < bestEnergy:
                                    bestState = copy.deepcopy(state)
                                    bestEnergy = E
                    if updates > 1:
                            if step // updateWavelength > (step-1) // updateWavelength:
                                    update(T, E, float(accepts)/trials, float(improves)/trials)
                                    trials, accepts, improves = 0, 0, 0
		
		# Return best state and energy
                self.lienzo.annealingCompleted=True
		#return bestState, bestEnergy
                