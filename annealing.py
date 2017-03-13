#!/usr/bin/env python

""" Traveling salesman problem solved using Simulated Annealing.
"""
from scipy import *
from pylab import *
import numpy as np
import sys
import math
import re
import timing

def Distance(R1, R2):
    return sqrt((R1[0]-R2[0])**2+(R1[1]-R2[1])**2)

def TotalDistance(city, R):
    dist=0
    for i in range(len(city)-1):
        dist += Distance(R[city[i]],R[city[i+1]])
    dist += Distance(R[city[-1]],R[city[0]])
    return dist
    
def reverse(city, n):
    nct = len(city)
    nn = (1+ ((n[1]-n[0]) % nct))/2 # half the lenght of the segment to be reversed
    # the segment is reversed in the following way n[0]<->n[1], n[0]+1<->n[1]-1, n[0]+2<->n[1]-2,...
    # Start at the ends of the segment and swap pairs of cities, moving towards the center.
    for j in range(nn):
        k = (n[0]+j) % nct
        l = (n[1]-j) % nct
        (city[k],city[l]) = (city[l],city[k])  # swap
    
def transpt(city, n):
    nct = len(city)
    
    newcity=[]
    # Segment in the range n[0]...n[1]
    for j in range( (n[1]-n[0])%nct + 1):
        newcity.append(city[ (j+n[0])%nct ])
    # is followed by segment n[5]...n[2]
    for j in range( (n[2]-n[5])%nct + 1):
        newcity.append(city[ (j+n[5])%nct ])
    # is followed by segment n[3]...n[4]
    for j in range( (n[4]-n[3])%nct + 1):
        newcity.append(city[ (j+n[3])%nct ])
    return newcity

def Plot(city, R, dist):
    # Plot
    Pt = [R[city[i]] for i in range(len(city))]
    Pt += [R[city[0]]]
    Pt = array(Pt)
    title('Total distance='+str(dist))
    plot(Pt[:,0], Pt[:,1], '-o')
    show()

class City:
	def __init__(self, cid, x, y):
		self.cid = cid
		self.x = x
		self.y = y
	def as_array(self):
		return [int(self.x), int(self.y)]

if __name__=='__main__':

    maxTsteps = 100    # Temperature is lowered not more than maxTsteps
    Tstart = 0.2       # Starting temperature - has to be high enough
    fCool = 0.9        # Factor to multiply temperature at each cooling step

    Preverse = 0.5      # How often to choose reverse/transpose trial move

    listofCitiesObjs = []

    nc = 100 #10,25,50,100
    for i in range(1, 26):
        target = open ("citydata/" + str(nc) + "-cities-no-" + str(i), "r")
        ncities = int(target.readline().strip()[1:-1])
        cities = []
        for i in range(0, int(ncities)):
            citydat = re.sub('[<>]', '', target.readline()).split()
            citycurr = City(citydat[0], citydat[1], citydat[2])
            cities.append(citycurr)
        target.close()
        listofCitiesObjs.append(cities)

    timing.main()

    for currcitylist in listofCitiesObjs:

        R = list(map(City.as_array, currcitylist))
        maxSteps = 100*ncities     # Number of steps at constant temperature
        maxAccepted = 10*ncities   # Number of accepted steps at constant temperature

        # The index table -- the order the cities are visited.
        city = range(ncities)
        # Distance of the travel at the beginning
        dist = TotalDistance(city, R)

        # Stores points of a move
        n = zeros(6, dtype=int)
        nct = len(R) # number of cities
    
        T = Tstart # temperature

        Plot(city, R, dist)
    
        for t in range(maxTsteps):  # Over temperature
    
            accepted = 0
            for i in range(maxSteps): # At each temperature, many Monte Carlo steps
            
                while True: # Will find two random cities sufficiently close by
                    # Two cities n[0] and n[1] are choosen at random
                    n[0] = int((nct)*rand())     # select one city
                    n[1] = int((nct-1)*rand())   # select another city, but not the same
                    if (n[1] >= n[0]): n[1] += 1   #
                    if (n[1] < n[0]): (n[0],n[1]) = (n[1],n[0]) # swap, because it must be: n[0]<n[1]
                    nn = (n[0]+nct -n[1]-1) % nct  # number of cities not on the segment n[0]..n[1]
                    if nn>=3: break
        
                # We want to have one index before and one after the two cities
                # The order hence is [n2,n0,n1,n3]
                n[2] = (n[0]-1) % nct  # index before n0  -- see figure in the lecture notes
                n[3] = (n[1]+1) % nct  # index after n2   -- see figure in the lecture notes
            
                if Preverse > rand(): 
                    # Here we reverse a segment
                    # What would be the cost to reverse the path between city[n[0]]-city[n[1]]?
                    de = Distance(R[city[n[2]]],R[city[n[1]]]) + Distance(R[city[n[3]]],R[city[n[0]]]) - Distance(R[city[n[2]]],R[city[n[0]]]) - Distance(R[city[n[3]]],R[city[n[1]]])
                
                    if de<0 or exp(-de/T)>rand(): # Metropolis
                        accepted += 1
                        dist += de
                        reverse(city, n)
                else:
                    # Here we transpose a segment
                    nc = (n[1]+1+ int(rand()*(nn-1)))%nct  # Another point outside n[0],n[1] segment. See picture in lecture nodes!
                    n[4] = nc
                    n[5] = (nc+1) % nct
        
                    # Cost to transpose a segment
                    de = -Distance(R[city[n[1]]],R[city[n[3]]]) - Distance(R[city[n[0]]],R[city[n[2]]]) - Distance(R[city[n[4]]],R[city[n[5]]])
                    de += Distance(R[city[n[0]]],R[city[n[4]]]) + Distance(R[city[n[1]]],R[city[n[5]]]) + Distance(R[city[n[2]]],R[city[n[3]]])
                
                    if de<0 or exp(-de/T)>rand(): # Metropolis
                        accepted += 1
                        dist += de
                        city = transpt(city, n)
                    
                if accepted > maxAccepted: break

            # Plot
            Plot(city, R, dist)
            
            print "T=%10.5f , distance= %10.5f , accepted steps= %d" %(T, dist, accepted)
            T *= fCool             # The system is cooled down
            if accepted == 0: break  # If the path does not want to change any more, we can stop

        
        Plot(city, R, dist)
        timing.log("clawk.")
    
