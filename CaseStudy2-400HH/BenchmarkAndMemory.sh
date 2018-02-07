#! /bin/bash
#############################################################
#                    Performance study                      #
pushd BRIAN  >/dev/zero  && echo "=== BRIAN ===" && \
	{
	python example.py &	RUNPID="$!"
	top -b -p $RUNPID > BRIAN.stat & TOPPID="$!"
	wait $RUNPID
	kill $TOPPID
	} &&\
	popd >/dev/zero

pushd NEURON >/dev/zero && echo "== NEURON ==" && \
#	nrngui -nogui -python -istty example.py
	{
	python example.py &	RUNPID="$!"
	top -b -p $RUNPID > NEURON.stat & TOPPID="$!"
	wait $RUNPID
	kill $TOPPID
	} &&\
	popd >/dev/zero

pushd NEST   >/dev/zero && echo "=== NEST ===" && 
	{
	python example.py &	RUNPID="$!"
	top -b -p $RUNPID > NEST.stat & TOPPID="$!"
	wait $RUNPID
	kill $TOPPID
	} &&\
	popd >/dev/zero


#############################################################
#                    LOF NOC study                         #

pushd BRIAN  >/dev/zero  && echo "=== BRIAN ===" && \
    cat example.py | sed '/^\s*$/d;/^\s#/d' | wc -lc && \
    popd >/dev/zero

pushd NEURON >/dev/zero && echo "== NEURON ==" && \
	cat example.py exp2syn.mod expsyn.mod hh.mod | sed "/^\s*$/d" | wc -lc && \
    popd >/dev/zero

pushd NEST   >/dev/zero && echo "=== NEST ===" && 
    cat example.py hh_psc_alpha.cpp hh_psc_alpha.h | sed "s|//.*$||g;/^\s*$/d" |wc -cl && \
    popd >/dev/zero

#############################################################
