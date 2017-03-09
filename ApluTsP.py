import numpy as np
import sys
import math
import re

class City:
	def __init__(self, cid, x, y):
		self.cid = cid
		self.x = x
		self.y = y
	def as_vector(self):
		return [self.x, self.y]

target = open('citydata/10-cities-no-1', 'r')
ncities = target.readline().strip()[1:-1]

cities = []
for i in range(0, int(ncities)):
	citydat = re.sub('[<>]', '', target.readline()).split()
	citycurr = City(citydat[0], citydat[1], citydat[2])
	cities.append(citycurr)

target.close()

print "Starting from", cities[0].as_vector(), "to explore", ncities, "cities."

def euclidian(vector1, vector2):
	dist = [(a - b)**2 for a, b in zip(vector1, vector2)]
	dist = math.sqrt(sum(dist))
	return dist
