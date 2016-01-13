import matplotlib.pyplot as plt
import numpy as np

import numpy.random as nr
def gausserr(scale):
    if scale <= 0:
        return 0
    else:
        return nr.normal(scale=scale)

class Tracker(object):
    def __init__(self,offsetpiezo,sampleTimeCourse,dzerr=0.0):
        self.piezo = offsetpiezo
        self.stc = sampleTimeCourse
        self.dzerr=dzerr
        self.history = []

    def opInit(self,pos):
        self.piezo.MoveTo(0,pos)
        self.calibpos = pos
        self.lastAdjustment = 0
        self.previoushistory = self.history
        self.history = []
        
    def compare(self,tick):
        samplez = self.stc.z(tick)
        focus = self.piezo.focus()

        posDelta = self.piezo.GetPos(0) - self.calibpos
        dz = focus - samplez + gausserr(self.dzerr)
        if self.useposDelta:
            if self.addDelta:
                return dz + posDelta
            else:
                return dz - posDelta
        else:
            return dz

    def track(self,tolerance,minDelay=5, useposDelta=False, addDelta=True):
        self.minDelay = minDelay
        self.focusTolerance = tolerance
        self.useposDelta = useposDelta
        self.addDelta = addDelta

        # if we had previous runs the nominal pos can already
        # be contaminated, we should somehow reset the offset
        # and get pos back to where it should be.
        self.opInit(self.stc.z(0))
        for tick in range(self.stc.ntics):
            t = self.stc.t(tick)
            dz = self.compare(tick)
            self.history.append((t, dz, self.piezo.GetOffset(), self.piezo.GetPos(0),
                                 self.stc.z(tick), self.piezo.focus()))
            if abs(dz) > self.focusTolerance and self.lastAdjustment >= self.minDelay:
                zcorr = self.piezo.GetOffset() - dz
                self.piezo.SetOffset(zcorr)
                self.lastAdjustment = 0
            else:
                self.lastAdjustment += 1

    def plothistory(self):
        t, dz, poffset, pos, samplez, focus  = np.array(self.history).T
        
        plt.subplot(4,1,1)
        plt.plot(t,dz)
        plt.title('dz')

        plt.subplot(4,1,2)
        plt.plot(t,poffset)
        plt.plot(t,pos)
        plt.title('offset & pos')

        plt.subplot(4,1,3)
        plt.plot(t,samplez)
        plt.plot(t,focus)
        plt.title('sample vs tracked focus')

        plt.subplot(4,1,4)
        plt.plot(t,focus-samplez)
        plt.title('tracked focus - sample pos')
        plt.show()

class TrackerCmdTC(Tracker):
    def __init__(self,offsetpiezo,sampleTimeCourse, cmdTimeCourse, dzerr=0.0):
        self.cmdTC = cmdTimeCourse
        super(self.__class__, self).__init__(offsetpiezo,sampleTimeCourse,dzerr)

    def compare(self,tick):
        samplez = self.stc.z(tick)
        focus = self.piezo.focus()

        posDelta = self.cmdTC.z(tick) - self.calibpos
        dz = focus - samplez
        return dz - posDelta + gausserr(self.dzerr)

    def plothistory(self):
        t, dz, poffset, pos, samplez, focus  = np.array(self.history).T
        
        plt.subplot(4,1,1)
        plt.plot(t,dz)
        plt.title('dz')

        plt.subplot(4,1,2)
        plt.plot(t,poffset)
        plt.plot(t,pos)
        plt.title('offset & pos')

        plt.subplot(4,1,3)
        plt.plot(t,samplez)
        plt.plot(t,focus)
        plt.title('sample vs tracked focus')

        plt.subplot(4,1,4)
        plt.plot(t,focus-samplez)
        plt.plot(self.cmdTC._t,self.cmdTC._z)
        plt.title('tracked focus - sample pos')
        plt.show()
