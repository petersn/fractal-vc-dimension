
CPPFLAGS=-Wall -g -fPIC -O3 -ffast-math -std=c++11

all: libsearch.so

lib%.so: %.o
	g++ -shared -Wl,-soname,$@ $< -o $@

.PHONY: clean
clean:
	rm -f *.o *.so

