import numpy as np

class sampleTC():
    def __init__(self,ntics,amp=50,period=100,mode='sin',rawz=None):
        self.ntics = ntics
        self.amp = amp
        self.period = period
        self.mode = mode
        self.rawz = rawz
        self.initialise()

    def initialise(self):
        self._t = np.arange(self.ntics)
        if self.mode == 'sin':
            self._z = self.amp*np.sin(self._t*2*np.pi/self.period)
        elif self.mode == 'sawtooth':
            self._z = self.amp/float(self.period)*(self._t % self.period)
        elif self.mode == 'raw':
            self._z = self.rawz
            self.ntics = self._z.shape[0]
            self._t = np.arange(self.ntics)
        else:
            raise("unsupported mode '%s'" % (self.mode))

    def t(self,pos=0):
        return self._t[pos]

    def z(self,pos=0):
        return self._z[pos]
