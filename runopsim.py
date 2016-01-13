import matplotlib.pyplot as plt
import TrackerSim as Tracker
from sampleTimeCourse import sampleTC
import opsim

bp = opsim.rawpiezoSimNoisy(readerr=5.0,moverr=10.0)
op = opsim.piezoOffsetSim(bp)

sampletc = sampleTC(10000,amp=100,period=2000)
cmdtc = sampleTC(10000,amp=10,period=2500,mode='sawtooth')

plot(sampletc._t,sampletc._z)
show()

# tr = Tracker.Tracker(op,sampletc,dzerr=10.0)
tr = Tracker.TrackerCmdTC(op,sampletc,cmdtc,dzerr=10.0)
tr.track(tolerance=50,minDelay=50,useposDelta=True)
t, dz, poffset, pos, samplez, focus  = np.array(tr.history).T
tr.plothistory()
