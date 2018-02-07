import time, sys
import numpy as np
import matplotlib
matplotlib.rcParams["savefig.directory"] = ""
from matplotlib import pyplot as plt
from neuron import h


startbuild=time.time()
class neuron:
	def __init__(self,v):
		self.soma = h.Section()
		self.soma.L		= 200.
		self.soma.diam	= 20./np.pi
		self.soma.nseg	= 1
		self.soma.insert('hh')
		self.soma(0.5).el_hh = -30.3
		self.soma(0.5).v = v
		self.isyn	= h.Exp2Syn(0.5, sec=self.soma)
		self.isyn.e		= -75.0
		self.isyn.tau1	= 0.99
		self.isyn.tau2	= 1.0
		self.esyn	= h.ExpSyn(0.5, sec=self.soma)
		self.esyn.e		= 0.0
		self.esyn.tau	= 0.8
		self.spks	= h.Vector()
		self.sptr	= h.APCount(.5, sec=self.soma)
		self.sptr.thresh = 25
		self.sptr.record(self.spks)

		
#neurons = [ neuron(v) for v in np.random.randn(400)*50.-50. ]
neurons = [ neuron(v) for v in np.genfromtxt("../volt.ssv") ]

conlist = list(np.genfromtxt("../connections.ssv").astype(int))

connections=[ h.NetCon(neurons[pre].soma(0.5)._ref_v,neurons[post].isyn, 25., 3.0, 0.2, sec=neurons[pre].soma)\
				for pre,cs in enumerate(conlist) for post in list(cs) ]

h.dt = 0.05
h.finitialize()
h.fcurrent()
h.frecord_init()
endbuild=time.time()

while h.t < 500.:h.fadvance()

endsimulate= time.time()


print("Building time     : %.2f s"%(endbuild-startbuild ))
print("Simulation time   : %.2f s"%(endsimulate-endbuild))
print("Time step         : %.2f ms"%(h.dt))

spks = []
for ni, n in enumerate(neurons):
	spk = list(np.array(n.spks))
	for sp in spk:
		spks.append((sp,ni))

spks = np.array(spks)
plt.plot(spks[:,0],spks[:,1],".k",ms=9)
plt.xlim(0.,500.)
plt.show()


exit(0)
