import time
import numpy as np
import matplotlib
matplotlib.rcParams["savefig.directory"] = ""
from matplotlib import pyplot as plt
import nest

startbuild=time.time()

nest.ResetKernel()
nest.SetKernelStatus({"resolution": 0.05})

vinit=[ x for x in np.genfromtxt("../volt.ssv") ]
nest.SetDefaults("hh_psc_alpha", { 'E_L':-30.3, 'tau_syn_in':1. } )
neurons = nest.Create("hh_psc_alpha",400)
for n in neurons:
	nest.SetStatus([neurons[n-1]],{'V_m' : vinit[n-1] })

nest.CopyModel("static_synapse","excitatory",{"weight":1.,  "delay":1.5})
nest.CopyModel("static_synapse","inhibitory",{"weight":200., "delay":3.0})

conlist = list(np.genfromtxt("../connections.ssv").astype(int))
conpairs = [([pre]*len(post), post) for pre, post in enumerate(conlist)]
pre, post = zip(*conpairs)

nest.Connect(np.array(neurons)[np.array(pre).flatten()], np.array(neurons)[np.array(post).flatten()], 'one_to_one', syn_spec="inhibitory")

ispikes  = nest.Create("spike_detector")
nest.SetStatus(ispikes,[{"label": "hh-inhibitory",
                         "withtime": True,
                         "withgid": True,
                         "to_file": False}])

nest.Connect(neurons, ispikes, syn_spec="excitatory")

endbuild=time.time()

nest.Simulate(499.5)

endsimulate= time.time()

print("Building time     : %.2f s"%(endbuild-startbuild ))
print("Simulation time   : %.2f s"%(endsimulate-endbuild))
print("Time step         : %.2f ms"%(nest.GetKernelStatus()['resolution']))


ev = nest.GetStatus(ispikes, "events")[0]
ispikes = np.dstack((ev["times"], ev["senders"]    ))[0]

plt.plot(ispikes[:,0],ispikes[:,1],".k",ms=9)
plt.xlim(0.,500.)

plt.show()
