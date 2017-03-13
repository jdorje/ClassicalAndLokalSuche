import numpy as np
import sys
import math
import re

#class Knoten:

class City:
	def __init__(self, cid, x, y):
		self.cid = cid
		self.x = x
		self.y = y
	def as_tuple(self):
		return (int(self.x), int(self.y))

def euclidian(vector1, vector2):
	return ((vector1[0] - vector2[0])**2 + (vector1[1] - vector2[1])**2) ** 0.5

def mk_matrix(coord, dist):
    """Compute a distance matrix for a set of points.

    Uses function 'dist' to calculate distance between
    any two points.  Parameters:
    -coord -- list of tuples with coordinates of all points, [(x1,y1),...,(xn,yn)]
    -dist -- distance function
    """
    n = len(coord)
    D = {}      # dictionary to hold n times n matrix
    for i in range(n-1):
        for j in range(i+1,n):
            D[i,j] = dist(coord[i], coord[j])
            D[j,i] = D[i,j]
    return D

def length(tour, D):
    """Calculate the length of a tour according to distance matrix 'D'."""
    z = D[tour[-1], tour[0]]    # edge from last to first city of the tour
    for i in range(1,len(tour)):
        z += D[tour[i], tour[i-1]]      # add length of edge from city i-1 to i
    return z

def nearest(last, unvisited, D):
    """Return the index of the node which is closest to 'last'."""
    near = unvisited[0]
    min_dist = D[last, near]
    for i in unvisited[1:]:
        if D[last,i] < min_dist:
            near = i
            min_dist = D[last, near]
    return near

def nearest_neighbor(n, i, D):
    """Return tour starting from city 'i', using the Nearest Neighbor.

    Uses the Nearest Neighbor heuristic to construct a solution:
    - start visiting city i
    - while there are unvisited cities, follow to the closest one
    - return to city i
    """
    unvisited = range(n)
    unvisited.remove(i)
    last = i
    tour = [i]
    while unvisited != []:
        next = nearest(last, unvisited, D)
        tour.append(next)
        unvisited.remove(next)
        last = next
    return tour

if __name__ == "__main__":
	target = open('citydata/10-cities-no-1', 'r')
	ncities = int(target.readline().strip()[1:-1])
	cities = []
	for i in range(0, int(ncities)):
		citydat = re.sub('[<>]', '', target.readline()).split()
		citycurr = City(citydat[0], citydat[1], citydat[2])
		cities.append(citycurr)
	target.close()


	#print "Starting from", cities[0].as_tuple(), "to explore", ncities, "cities."

	coords = list(map(City.as_tuple, cities))
	matr = mk_matrix(coords, euclidian)

	closedset = [] #Nodes that haver been fully evaluated
	openset = [] #"Border" nodes

	openset.append(cities[0])
	closedset.extend(cities[1:])

	for o in openset:
		nn = nearest_neighbor(ncities, 0, matr)
		lenn = length(nn, matr)
		print lenn, nn
		# looks to be more a basis of simulated annealing than A* at this point
