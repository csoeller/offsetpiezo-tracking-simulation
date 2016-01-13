# -*- coding: utf-8 -*-

import eventLogSim as eventLog

class rawpiezoSim(object):
    def __init__(self):
        self._pos = 0

    def MoveTo(self, iChannel, fPos, bTimeOut=True):
        self.SetPos(fPos)
        
    def GetPos(self, iChannel=0):
        return self._pos

    def SetPos(self, fpos, iChannel=0):
        self._pos = fpos


import numpy.random as nr
def gausserr(scale):
    if scale <= 0:
        return 0
    else:
        return nr.normal(scale=scale)

class rawpiezoSimNoisy(rawpiezoSim):
    def __init__(self,readerr=0.0,moverr=0.0):
        super(self.__class__, self).__init__()
        self.readerr=readerr
        self.moverr=moverr

    def MoveTo(self, iChannel, fPos, bTimeOut=True):
        self.SetPos(fPos+gausserr(self.moverr))
        
    def GetPos(self, iChannel=0):
        return self._pos+gausserr(self.readerr)

class piezoOffsetSim():    
    def __init__(self, basePiezo):
        self.basePiezo = basePiezo
        self.offset = 0
        #self.driftQueue = Queue.Queue()

    # def ReInit(self):
    #     return self.basePiezo.ReInit()
        
    # def SetServo(self,val = 1):
    #     return self.basePiezo.SetServo(val)
        
    def MoveTo(self, iChannel, fPos, bTimeOut=True):
        return self.basePiezo.MoveTo(iChannel, fPos + self.offset, bTimeOut)
            
    # def MoveRel(self, iChannel, incr, bTimeOut=True):
    #     return self.basePiezo.MoveRel(iChannel, incr, bTimeOut)

    def GetPos(self, iChannel=0):
        return self.basePiezo.GetPos(iChannel) - self.offset
        
    # def GetControlReady(self):
    #     return self.basePiezo.GetControlReady()
         
    # def GetChannelObject(self):
    #     return self.basePiezo.GetChannelObject()
        
    # def GetChannelPhase(self):
    #     return self.basePiezo.GetChannelPhase()
        
    # def GetMin(self,iChan=1):
    #     return self.basePiezo.GetMin(iChan)
        
    # def GetMax(self, iChan=1):
    #     return self.basePiezo.GetMax(iChan)
        
    # def GetFirmwareVersion(self):
    #     return self.basePiezo.GetFirmwareVersion()
        
    def GetOffset(self):
        return self.offset
        
    def SetOffset(self, val):
        p = self.GetPos()
        self.offset = val
        self.MoveTo(0, p)
        
    def ZeroOffset(self):
        p = self.GetPos()
        p += self.offset
        self.offset = 0
        self.MoveTo(0, p)

    def LogShifts(self, dx, dy, dz):
        eventLog.logEvent('ShiftMeasure', '%3.4f, %3.4f, %3.4f' % (dx, dy, dz))
        #self.driftQueue.put((dx, dy, dz, time.time()))

    def focus(self):
        f = self.GetPos()
        f += self.offset
        # this is actually the position of the basepiezo and
        # the following should be true:
        #   f == self.basePiezo.GetPos(iChannel)
        # in fact it may be clearer to return that directly
        return f

def main():
    '''For testing only'''
    print 'foo'
    #st.run()
    #st.daemon.requestLoop()
    print 'bar'
    
if __name__ == '__main__':
    main()
