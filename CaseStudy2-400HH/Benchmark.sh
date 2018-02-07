#! /bin/bash
#############################################################
#                    Performance study                      #
pushd BRIAN  >/dev/zero  && echo "=== BRIAN ===" && \
	python example.py 
	popd >/dev/zero

pushd NEURON >/dev/zero && echo "== NEURON ==" && \
	nrngui -nogui -python -istty example.py
	popd >/dev/zero

pushd NEST   >/dev/zero && echo "=== NEST ===" && 
	python example.py
	popd >/dev/zero


#############################################################
#                    LOF NOC study                         #

pushd BRIAN  >/dev/zero  && echo "=== BRIAN ===" && \
    cat example.py | sed '/^\s*$/d;/^\s#/d' | wc -lc && \
    popd >/dev/zero

pushd NEURON >/dev/zero && echo "== NEURON ==" && \
	cat example.py exp2syn.mod hh.mod | sed "/^\s*$/d" | wc -lc && \
    popd >/dev/zero

pushd NEST   >/dev/zero && echo "=== NEST ===" && 
    cat example.py hh_psc_alpha.cpp hh_psc_alpha.h | sed "s|//.*$||g;/^\s*$/d" |wc -cl && \
    popd >/dev/zero

#############################################################
