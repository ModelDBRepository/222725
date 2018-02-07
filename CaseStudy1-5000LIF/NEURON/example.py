import time, sys
import numpy as np
import matplotlib
matplotlib.rcParams["savefig.directory"] = ""
from matplotlib import pyplot as plt
from neuron import h

startbuild=time.time()

Ne,Ni,Ns=4000,1000,500

excw,excd =  0.009, 0.8
inhw,inhd = -0.050, 2.1
stmw,stmd =  0.025, 0.5
inspk = np.genfromtxt("../input.ssv")

class liaf:
	def __init__(self):
		self.cell = h.IntFire1()
		self.cell.m = 0.
		self.recorder = h.NetCon(self.cell,None)
		self.spk = h.Vector()
		self.recorder.record(self.spk)

class stim:
	def __init__(self,sid):
		self.s          = h.VecStim()
		self.nvec       = inspk[np.where(inspk[:,1].astype(int) == sid),0][0]
		self.vec        = h.Vector(self.nvec.shape[0])
		self.vec.from_python(self.nvec)
		self.s.play(self.vec)
		self.recorder = h.NetCon(self.s,None)
		self.spk = h.Vector()
		self.recorder.record(self.spk)
		

E=[ liaf() for x in xrange(Ne) ]
I=[ liaf() for x in xrange(Ni) ]
S=[ stim(x) for x in xrange(Ns) ]

econs,icons,scons =[],[],[]

for pre,post in np.genfromtxt("../ee.ssv").astype(int):
	econs.append( h.NetCon(E[pre].cell,E[post].cell) )

for pre,post in np.genfromtxt("../ei.ssv").astype(int):
	econs.append( h.NetCon(E[pre].cell,I[post].cell) )
	
for pri,post in np.genfromtxt("../ie.ssv").astype(int):
	icons.append( h.NetCon(I[pri].cell,E[post].cell) )
for pri,post in np.genfromtxt("../ii.ssv").astype(int):
	icons.append( h.NetCon(I[pri].cell,I[post].cell) )

for prs,post in np.genfromtxt("../se.ssv").astype(int):
	scons.append( h.NetCon(S[prs].s  ,E[post].cell) )

sys.stderr.write("====== Network Created! =======\n")

for econ in econs:
	econ.weight[0],econ.delay = excw,excd
for icon in icons:
	icon.weight[0],icon.delay = inhw,inhd
for scon in scons:
	scon.weight[0],scon.delay = stmw,stmd

h.dt = 0.1
h.finitialize()
h.fcurrent()
h.frecord_init()

endbuild=time.time()

while h.t < 1000.:h.fadvance()

endsimulate= time.time()


print("Building time     : %.2f s"%(endbuild-startbuild ))
print("Simulation time   : %.2f s"%(endsimulate-endbuild))
print("Time step         : %.2f ms"%(h.dt))

spkse = np.array( [ (x,ni      ) for ni, nE in enumerate(E) for x in list(np.array(nE.spk)) ] )
spksi = np.array( [ (x,ni+Ne   +100) for ni, nI in enumerate(I) for x in list(np.array(nI.spk)) ] )
spkss = np.array( [ (x,ni+Ne+Ni+200) for ni, nS in enumerate(S) for x in list(np.array(nS.spk)) ] )

spkse = spkse[np.where(spkse[:,0]<200)]
spksi = spksi[np.where(spksi[:,0]<200)]
spkss = spkss[np.where(spkss[:,0]<200)]

plt.plot(spkse[:,0],spkse[:,1],"k.")
plt.plot(spksi[:,0],spksi[:,1],"r.")
plt.plot(spkss[:,0],spkss[:,1],"b.")

plt.show()

exit(0)
