#!/usr/bin/python

import ctypes
from ctypes import c_int, c_double, POINTER

dll = ctypes.CDLL("./libsearch.so")

# extern "C" int find_interesting_point(int label, double neighborhood_scale, double* result, int iters);
_find_interesting_point = dll.find_interesting_point
_find_interesting_point.restype = c_int
_find_interesting_point.argtypes = [c_int, c_double, POINTER(c_double), c_int]

# extern "C" void find_perturbations(int N, double* coefs, double scale, int iters, int verify_iters, int* table, double* offsets_table, int rounds);
find_perturbations = dll.find_perturbations
find_perturbations.restype = None
find_perturbations.argtypes = [c_int, POINTER(c_double), c_double, c_int, c_int, POINTER(c_int), POINTER(c_double), c_int]

# void initialize();
initialize = dll.initialize
initialize.restype = None
initialize.argtypes = []

# Actually do the initialization.
initialize()

def find_interesting_point(label, neighborhood_scale, iters):
	result = (c_double * 2)()
	points_tested = _find_interesting_point(label, neighborhood_scale, result, iters)
	#print "Tested:", points_tested
	z = result[0] + 1j * result[1]
	return z

class Searcher:
	def __init__(self, points):
		self.points = points
		self.N = len(points)
		self.coefs_buf = (c_double * (2 * self.N))()
		for i, z in enumerate(self.points):
			self.coefs_buf[2*i] = z.real
			self.coefs_buf[2*i+1] = z.imag
		self.table_buf = (c_int * (2**self.N))()
		for i in xrange(2**self.N):
			self.table_buf[i] = 0
		self.offsets_table_buf = (c_double * (2 * 2**self.N))()
		for i in xrange(2 * 2**self.N):
			self.offsets_table_buf[i] = 0.0

	def get_table(self):
		return self.table_buf[:2**self.N]

	def fraction_shattered(self):
		table = self.get_table()
		return sum(i != 0 for i in table) / float(len(table))

	def get_offsets_table(self):
		pairs = zip(*[iter(self.offsets_table_buf[:2*2**self.N])]*2)
		return map(lambda (re, im): complex(re, im), pairs)

	def find_perturbations(self, scale, iters, verify_iters, rounds):
		find_perturbations(self.N, self.coefs_buf, scale, iters, verify_iters, self.table_buf, self.offsets_table_buf, rounds)

