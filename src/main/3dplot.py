'''
Created on 24 Nov 2015

@author: david
'''
import numpy as np
import particle as p
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

l = [[],[],[]]
for i in xrange(int(1e4)):
    x = p.Pion(500)
    a = x.Decay()
    if x.exit == False:
        if x.type == "e":
            pass
        else:
            b = a.Decay()
            if b != None:
                y = b.ExitPosition()
                l[0].append(y[0])
                l[1].append(y[1])
                l[2].append(y[2])


fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', projection='3d')
ax.scatter(l[0],l[1],l[2])
plt.show()
