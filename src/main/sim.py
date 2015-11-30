'''
Created on 17 Nov 2015

@author: david
'''

import numpy as np
from particle import Pion
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import constants as constants

def PlotHistogram(data):
    hist, bins = np.histogram(data, bins = 50)
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()

class Simulation:
    const = constants.Constants()
    def __init__(self, position):
        self.detector = constants.Detector(position)
    def ParticleSimExit(self, energy):
        '''Returns position of final particle's exit from detector'''
        pi = Pion(energy)
        if pi.DecayCheck(self.const.dimensions) == False:
            decay_part = pi.Decay()
            if pi.type == 'e':
                return 'electron', decay_part.ExitPosition()
            else:
                mu = decay_part
                if mu.DecayCheck(self.const.dimensions) == False:
                    el = mu.Decay()
                    return 'muon-electron', el.ExitPosition()
                else:
                    return 'muon', mu.ExitPosition()
        else:
            return 'pion', pi.exit_pos    
    def ParticleSimDetect(self, energy):
        pi = Pion(energy)
        if pi.DecayCheck(np.array([2.5,self.detector.position[2]+0.3])) == False:
            decay_part = pi.Decay()
            if pi.type == 'e':
                return decay_part.EnergyDeposited(self.detector)
            else:
                mu = decay_part
                if mu.DecayCheck(np.array([2.5,self.detector.position[2]+0.3])) == False:
                    el = mu.Decay()
                    return el.EnergyDeposited(self.detector)
                else:
                    return mu.EnergyDeposited(self.detector)
        else:
            return 0
    def ParticleSimEnergy(self, energy):
        pi = Pion(energy)
        if pi.DecayCheck(self.const.dimensions) == False:
            decay_part = pi.Decay()
            if pi.type == 'e':
                return 'electron', decay_part.energyvector.temporal
            else:
                mu = decay_part
                if mu.DecayCheck(self.const.dimensions) == False:
                    el = mu.Decay()
                    return 'muon-electron', el.energyvector.temporal
                else:
                    return 'muon', mu.energyvector.temporal
        else:
            return 'pion', pi.energyvector.temporal
    def PlotExit3D(self, n,energy):
        pi, mu, e, em = [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]
        for i in xrange(n):
            p_type, p_pos = self.ParticleSimExit(energy)
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
    def MuonFractionCalc(self, n, energy):
        left = float(0)
        decayed = float(0)
        for i in xrange(int(n)):
            p_type, p_pos = self.ParticleSimExit(energy)
            if p_type == 'muon':
                left += 1
            elif p_type == 'muon-electron':
                decayed += 1
        return decayed/left
    def PlotMuonFraction(self, n, energy_array):
        frac = []
        for i in energy_array:
            frac.append(self.MuonFractionCalc(n, i))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(energy_array,frac)
        ax.set_xscale('log')
        plt.show()
    def PlotEnergySpectra(self, n, energy):
        pi, mu, e, em = [],[],[],[]
        for i in xrange(int(n)):
            p_type, p_energy = self.ParticleSimEnergy(energy)
            if p_type == 'electron':
                e.append(p_energy)
            elif p_type == 'pion':
                pi.append(p_energy)
            elif p_type == 'muon':
                mu.append(p_energy)
            elif p_type == 'muon-electron':
                em.append(p_energy)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(pi)
        if len(e) > 0:
            ax.hist(e)
        ax.hist(mu, facecolor='green')
        ax.hist(em)
        plt.show()
    def PlotEnergyDeposited(self, n, energy):
        Ee,Em = np.empty(0), np.empty(0)
        for i in range(int(n)):
            e = self.ParticleSimDetect(500)
            if e != 0:
                if e > 2:                    
                    Ee = np.append(Ee,e)
                else:
                    Em = np.append(Em,e)
        print float(len(Ee))/float(len(Em))
        fig = plt.figure()
        ax = fig.add_subplot(2,1,1)
        ax.hist(Em, bins = 50)
        ax = fig.add_subplot(2,1,2)
        ax.hist(Ee, bins=50)
        plt.show()
        #PlotHistogram(Em)
    
def main():
    sim = Simulation(np.array([[1],[1],[9]]))
    #PlotExit3D(int(1e4), 1000)
    sim.PlotEnergySpectra(1e3, 500)
    #MuonFraction(1e1, np.logspace(np.log10(500),np.log10(1e4)))
      
if __name__ == '__main__':
    main()
