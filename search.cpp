// Fast searching.

using namespace std;
#include <iostream>
#include <random>
#include <complex>
#include <stdint.h>

typedef complex<double> Complex;

#define DIVISION_FACTOR 4

struct Random {
	random_device rd;
	mt19937 e2;
	uniform_real_distribution<> dist;
	uniform_real_distribution<> interesting_real;
	uniform_real_distribution<> interesting_imag;

	Random() : e2(rd()), dist(-1, 1), interesting_real(-1.5, 0.5), interesting_imag(-0.9, 0.9) {}
};

Random* global_random;

bool mandelbrot_test(Complex z, int iters) {
	Complex z0 = z;
	iters += DIVISION_FACTOR - 1;
	iters /= DIVISION_FACTOR;
	while (iters--) {
		for (int i = 0; i < DIVISION_FACTOR; i++)
			z = z*z + z0;
		if (abs(z) > 2.0)
			return false;
	}
	return true;
}

uint64_t compute_mask(int N, Complex* values, Complex offset, int iters) {
	uint64_t result = 0;
	for (int i = 0; i < N; i++) {
		bool hit = mandelbrot_test(values[i] + offset, iters);
		if (hit)
			result |= 1 << i;
	}
	return result;
}

extern "C" int find_interesting_point(int label, double neighborhood_scale, double* result, int iters) {
	int points_tested = 0;
	bool label_bool = label;
	while (true) {
		points_tested++;
		Complex z(global_random->interesting_real(global_random->e2), global_random->interesting_imag(global_random->e2));
		// We must find a point of the given label.
		if (mandelbrot_test(z, iters) != label_bool)
			continue;
		for (int i = 0; i < 16; i++) {
			Complex offset = Complex(global_random->dist(global_random->e2) * neighborhood_scale, global_random->dist(global_random->e2) * neighborhood_scale);
			Complex adjacent = z + offset;
			if (mandelbrot_test(adjacent, iters) != label_bool) {
				result[0] = z.real();
				result[1] = z.imag();
				return points_tested;
			}
		}
	}
}

extern "C" void find_perturbations(int N, double* coefs, double scale, int iters, int verify_iters, int* table, double* offsets_table, int rounds) {
	Complex* values = new Complex[N];
	for (int i = 0; i < N; i++)
		values[i] = Complex(coefs[2*i], coefs[2*i+1]);
	while (rounds--) {
		// Produce a random offset.
		Complex offset = Complex(global_random->dist(global_random->e2) * scale, global_random->dist(global_random->e2) * scale);
		uint64_t result = compute_mask(N, values, offset, iters);
		// Double check, if this is the first entry in the given bucket!
		if (table[result] == 0) {
			uint64_t double_check = compute_mask(N, values, offset, verify_iters);
			if (double_check != result) {
				//cout << "========== Error! Result didn't hold up under iteration." << endl;
				//cout << result << " vs " << double_check << endl;
				//cout << "At offset: " << offset << endl;
				continue;
			}
			// We have a first hit!
			offsets_table[2*result] = offset.real();
			offsets_table[2*result+1] = offset.imag();
		}
		// Now increment the bucket.
		table[result]++;
	}
	delete[] values;
}

extern "C" void initialize() {
	global_random = new Random();
}

