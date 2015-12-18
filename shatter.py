#!/usr/bin/python

import sys
import random
from matplotlib import pyplot as plt
import search

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

N = 12
neighborhood = 1e-6
search_scale = 3e-6
iters = 1000
rounds_per_attempt = 150000

class Attempt:
	def __init__(self):
		self.points = [search.find_interesting_point(True, neighborhood, iters) for i in xrange(N)]
		self.searcher = search.Searcher(self.points)
		self.total_rounds = 0
		#print "Percent shattered: %f%%" % (searcher.fraction_shattered() * 100.0)

	def do_work(self, rounds):
		self.searcher.find_perturbations(scale=search_scale, iters=iters, verify_iters=iters, rounds=rounds)
		self.total_rounds += rounds

attempts = []
while True:
	print "=== Beginning epoch."
	attempts.append(Attempt())
	print "Generated new attempt."
	for i, a in enumerate(attempts):
		print "\rDoing work: %i/%i" % (i+1, len(attempts)),
		sys.stdout.flush()
		a.do_work(rounds_per_attempt)
	print
	best_attempt = max(attempts, key=lambda a: a.searcher.fraction_shattered())
	index = attempts.index(best_attempt)
	print "Best attempt [%i/%i], with: %f%% shattered" % (index+1, len(attempts), best_attempt.searcher.fraction_shattered() * 100.0)

