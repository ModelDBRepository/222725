import time,sys
import numpy as np
from matplotlib import pyplot as plt
import nest

startbuild=time.time()
Ne,Ni,Ns=4000,1000,500

excw,excd =  0.009, 0.8
inhw,inhd = -0.050, 2.1
stmw,stmd =  0.025, 0.5
inspk = np.genfromtxt("../input.ssv")
inspk[:,0] += 1.

nest.ResetKernel()
nest.SetKernelStatus({"resolution": 0.1})

nest.SetDefaults("iaf_psc_delta", { 'E_L':0.,  'C_m':1., 'V_th':1., 'V_reset':0., 't_ref':5., } )
E = nest.Create("iaf_psc_delta",Ne)
I = nest.Create("iaf_psc_delta",Ni)
for n in E: nest.SetStatus([E[n-1]],{'V_m' : 0. })
for n in I: nest.SetStatus([I[n-1-Ne]],{'V_m' : 0. })
S = [ nest.Create("spike_generator",params={"spike_times": inspk[np.where(inspk[:,1].astype(int) == sid),0][0], 'allow_offgrid_spikes': True})[0] for sid in xrange(Ns) ]

nest.CopyModel("static_synapse","excitatory", {"weight":excw, "delay":excd} )
nest.CopyModel("static_synapse","inhibitory", {"weight":inhw, "delay":inhd} )
nest.CopyModel("static_synapse","stimulation",{"weight":stmw, "delay":stmd} )

pre, post = zip(*np.genfromtxt("../ee.ssv").astype(int))
nest.Connect(np.array(E)[np.array(pre)], np.array(E)[np.array(post)], 'one_to_one', syn_spec="excitatory")

pre, post = zip(*np.genfromtxt("../ei.ssv").astype(int))
nest.Connect(np.array(E)[np.array(pre)], np.array(I)[np.array(post)], 'one_to_one', syn_spec="excitatory")
sys.stderr.write("====== E connections Created! =======\n")

pre, post = zip(*np.genfromtxt("../ie.ssv").astype(int))
nest.Connect(np.array(I)[np.array(pre)], np.array(E)[np.array(post)], 'one_to_one', syn_spec="inhibitory")

pre, post = zip(*np.genfromtxt("../ii.ssv").astype(int))
nest.Connect(np.array(I)[np.array(pre)], np.array(I)[np.array(post)], 'one_to_one', syn_spec="inhibitory")
sys.stderr.write("====== I connections Created! =======\n")

pre, post = zip(*np.genfromtxt("../se.ssv").astype(int))
nest.Connect(np.array(S)[np.array(pre)], np.array(E)[np.array(post)], 'one_to_one', syn_spec="stimulation")

sys.stderr.write("====== Network Created! =======\n")


espk  = nest.Create("spike_detector")
nest.SetStatus(espk,[{"label": "liaf-e", "withtime": True, "withgid": True, "to_file": False}])
nest.Connect(E, espk, syn_spec="excitatory")

ispk  = nest.Create("spike_detector")
nest.SetStatus(ispk,[{"label": "lif-i", "withtime": True, "withgid": True, "to_file": False}])
nest.Connect(I, ispk, syn_spec="inhibitory")

sspk  = nest.Create("spike_detector")
nest.SetStatus(sspk,[{"label": "input", "withtime": True, "withgid": True, "to_file": False}])
nest.Connect(S, sspk, syn_spec="stimulation")

endbuild=time.time()

nest.Simulate(1000.)

endsimulate= time.time()

print("Building time     : %.2f s"%(endbuild-startbuild ))
print("Simulation time   : %.2f s"%(endsimulate-endbuild))
print("Time step         : %.2f ms"%(nest.GetKernelStatus()['resolution']))

ev = nest.GetStatus(espk, "events")[0]
spkse = np.dstack((ev["times"], ev["senders"]    ))[0]
ev = nest.GetStatus(ispk, "events")[0]
spksi = np.dstack((ev["times"], ev["senders"]+100))[0]
ev = nest.GetStatus(sspk, "events")[0]
spkss = np.dstack((ev["times"], ev["senders"]+200))[0]

spkse = spkse[np.where(spkse[:,0]<200)]
spksi = spksi[np.where(spksi[:,0]<200)]
spkss = spkss[np.where(spkss[:,0]<200)]

plt.plot(spkse[:,0],spkse[:,1],"k.")
plt.plot(spksi[:,0],spksi[:,1],"r.")
plt.plot(spkss[:,0],spkss[:,1],"b.")

plt.show()
