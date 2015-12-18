#!/usr/bin/python

import random
from matplotlib import pyplot as plt

def test(z, max_iters=400):
	z0 = z
	for i in xrange((max_iters+1)/2):
		z = (z**2 + z0)**2 + z0
		if abs(z) > 2:
			return False
	return True

def apply_isometry(iso, z):
	a, b = iso
	return a * z + b

def get_point(label, neighborhood):
	iters = 0
	while True:
		iters += 1
		re = random.uniform(-1, 0.5)
		im = random.uniform(-0.9, 0.9)
		z = re + 1j * im
		if test(z) != label:
			continue
		# Try to find an adjacent point of a different kind.
		for i in xrange(16):
			adjacent = z + random.uniform(-neighborhood, neighborhood) + 1j * random.uniform(-neighborhood, neighborhood)
			if test(adjacent) != label:
				print "Iterations:", iters
				return z

def plot_around(z, scale, pts=40):
	xs, ys = [], []
	for x in xrange(pts):
		for y in xrange(pts):
			offset = (((x - pts/2) + 1j * (y - pts/2))/float(pts)) * scale
			if test(z + offset):
				xs.append(x)
				ys.append(y)
	print "Doing scatter plot."
	plt.scatter(xs, ys)
	plt.show(True)

N = 6
neighborhood = 1e-4
search = 3e-3

points = [get_point(True, neighborhood) for i in xrange(N)]

print "Found:", points

# Now we classify.
cases = set()
samples = 0
while len(cases) < 2**N:
	shift = random.uniform(-search, search) + 1j * random.uniform(-search, search)
	new = [p + shift for p in points]
	cases.add(tuple(map(test, new)))
	samples += 1
print "Samples required to shatter:", samples

