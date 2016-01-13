
# coding: utf-8

# In[1]:

#get_ipython().magic(u'matplotlib notebook')

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(7,4))


# In[3]:

data = np.loadtxt('responsetracks.csv',delimiter=',')


# In[4]:

t = data[:,0]
pos = data[:,2]
xtrack = data[:,1]
plt.subplot(2,1,1)
plt.plot(t,pos)
plt.ylim(-100,100)
plt.ylabel('z (nm)')

plt.subplot(2,1,2)
plt.plot(t,xtrack)
plt.ylabel('x (nm)')
plt.ylim(-20,100)
plt.xlabel('time (s)')

plt.show()
# In[ ]:



