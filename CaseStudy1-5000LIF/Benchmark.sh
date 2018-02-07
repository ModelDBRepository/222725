#! /bin/bash
#############################################################
#                    Performance study                      #
pushd BRIAN  >/dev/zero  && echo "=== BRIAN ===" && \
	python example.py 
	popd >/dev/zero

pushd NEURON >/dev/zero && echo "== NEURON ==" && \
	nrnivmodl vecevent.mod && \
	nrngui -nogui -python -isatty  example.py 
	popd >/dev/zero

pushd NEST   >/dev/zero && echo "=== NEST ===" && \
	python example.py 
	popd >/dev/zero


#############################################################
#                    LOF NOC study                         #

pushd BRIAN  >/dev/zero  && echo "=== BRIAN ===" && \
	cat example.py | sed '/^\s*$/d;/^\s#/d' | wc -lc && \
	popd >/dev/zero

pushd NEURON >/dev/zero && echo "== NEURON ==" && \
	cat example.py intfire1.mod | sed "/^\s*$/d" | wc -lc && \
	popd >/dev/zero

pushd NEST   >/dev/zero && echo "=== NEST ===" && 
    cat example.py iaf_psc_delta.h iaf_psc_delta.cpp | sed "s|//.*$||g;/^\s*$/d" |wc -cl && \
    popd >/dev/zero

#############################################################
