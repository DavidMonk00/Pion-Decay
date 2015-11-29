'''
Created on 17 Nov 2015

@author: david
'''

import numpy as np
from particle import Pion
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def ParticleSim(energy):
    '''Returns position of final particle's exit from detector'''
    pi = Pion(energy)
    if pi.DecayCheck() == False:
        decay_part = pi.Decay()
        if pi.type == 'e':
            return 'electron', decay_part.ExitPosition()
        else:
            mu = decay_part
            if mu.DecayCheck() == False:
                el = mu.Decay()
                return 'muon-electron', el.ExitPosition()
            else:
                return 'muon', mu.ExitPosition()
    else:
        return 'pion', pi.exit_pos
         
def PlotExit3D(n,energy):
    pi = [[],[],[]]
    mu = [[],[],[]]
    e = [[],[],[]]
    em = [[],[],[]]
    for i in xrange(n):
        p_type, p_pos = ParticleSim(energy)
        if p_type == 'electron':
            e[0].append(p_pos[0])
            e[1].append(p_pos[1])
            e[2].append(p_pos[2])
        elif p_type == 'pion':
            pi[0].append(p_pos[0])
            pi[1].append(p_pos[1])
            pi[2].append(p_pos[2])
        elif p_type == 'muon':
            mu[0].append(p_pos[0])
            mu[1].append(p_pos[1])
            mu[2].append(p_pos[2])
        elif p_type == 'muon-electron':
            em[0].append(p_pos[0])
            em[1].append(p_pos[1])
            em[2].append(p_pos[2])  
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', projection='3d')
    ax.scatter(pi[0], pi[1], pi[2], c = 'g', s = 25)
    ax.scatter(mu[0], mu[1], mu[2], c = 'k', s = 1)
    ax.scatter(e[0], e[1], e[2], c = 'r', s = 25)
    ax.scatter(em[0], em[1], em[2], c = 'b', s = 25)
    plt.show()

def MuonFractionCalc(n, energy):
    left = float(0)
    decayed = float(0)
    for i in xrange(int(n)):
        p_type, p_pos = ParticleSim(energy)
        if p_type == 'muon':
            left += 1
        elif p_type == 'muon-electron':
            decayed += 1
    return decayed/left

def MuonFraction(n, energy_array):
    frac = []
    for i in energy_array:
        frac.append(MuonFractionCalc(n, i))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(energy_array,frac)
    ax.set_xscale('log')
    plt.show()
    
def main():
    #PlotExit3D(int(1e4), 1000)
    #print ParticleSim(500)
    MuonFraction(1e4, np.logspace(np.log10(500),np.log10(1e4)))
      
if __name__ == '__main__':
    main()
