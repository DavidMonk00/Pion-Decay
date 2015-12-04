'''
Created on 1 Dec 2015

@author: david
'''

from sim import Simulation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def PlotHistogram(data):
    hist, bins = np.histogram(data, bins = 50)
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()

class Plot:
    def __init__(self, position):
        self.sim = Simulation(position)
    def Exit3D(self, n,energy):
        pi, mu, e, em = [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]
        for i in xrange(n):
            p_type, p_pos = self.sim.ParticleExit(energy)
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
    def DecayPosition3D(self, n, energy):
        pi, mu = [[],[],[]], [[],[],[]]
        for i in xrange(int(n)):
            x = self.sim.ParticleDecay(energy)
            if len(x) == 2:
                pi[0].append(x[0][0])
                pi[1].append(x[0][1])
                pi[2].append(x[0][2])
                mu[0].append(x[1][0])
                mu[1].append(x[1][1])
                mu[2].append(x[1][2])
            elif len(x) == 1:
                pi[0].append(x[0][0])
                pi[1].append(x[0][1])
                pi[2].append(x[0][2])
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal', projection='3d')
        #ax.scatter(pi[0], pi[1], pi[2], c = 'g', s = 25)
        ax.scatter(mu[0], mu[1], mu[2], c = 'b', s = 10)
        plt.show()
    def DecayPosition1D(self, n, energy):
        pi, mu = [],[]
        for i in xrange(int(n)):
            x = self.sim.ParticleDecay(energy)
            if len(x) == 2:
                pi.append(float(x[0][2]))
                mu.append(float(x[1][2]))
            elif len(x) == 1:
                pi.append(float(x[0][2]))
        #print "Mean Pion decay position (in lab frame): ",sum(pi)/len(pi)
        #print "Mean Muon decay position (in lab frame): ",sum(mu)/len(mu)
        print sum(pi)/len(pi)
        print  sum(mu)/len(mu) - sum(pi)/len(pi)
        print len(pi)/len(mu)
        '''fig = plt.figure()
        ax = fig.add_subplot(2,1,1)
        ax.(pi, bins = 50)
        ax = fig.add_subplot(2,1,2)
        ax.hist(mu, bins = 50)
        plt.show()'''
    def MuonFraction(self, n, energy_array):
        frac = []
        for i in energy_array:
            frac.append(self.MuonFractionCalc(n, i))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(energy_array,frac)
        ax.set_xscale('log')
        plt.show()
    def EnergySpectra(self, n, energy):
        pi, mu, e, em = [],[],[],[]
        for i in xrange(int(n)):
            p_type, p_energy = self.sim.ParticleEnergy(energy)
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
    def EnergyDepositedDumb(self, n , energy):
        E = np.empty(0)
        for i in range(int(n)):
            e = self.sim.ParticleDetect(energy)
            if e != 0:
                print e
                E = np.append(E,e)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.hist(E, range=(min(E),max(E)), bins=50)
        plt.show()
        #PlotHistogram(Em)  
    def EnergyDepositedSmart(self, energy):
        Ee,Em,Eee = [],[],[]
        f = [x.strip() for x in open('/home/david/Python/data/010190/%s'%energy)]
        for i in f:
            e = float(i)
            if e > 140 and e < 150:
                Em.append(e)
            elif e < 140:
                Ee.append(e)
            else:
                Eee.append(e)
        print 'Separation complete'
        print (float(len(Eee))/float(len(Em)+len(Ee)))**-1
        fig = plt.figure()
        ax = fig.add_subplot(3,1,1)
        ax.hist(Em, range=(min(Em),max(Em)), bins=50)
        ax = fig.add_subplot(3,1,2)
        ax.hist(Ee, range=(min(Ee),max(Ee)), bins=50)
        ax = fig.add_subplot(3,1,3)
        ax.hist(Eee, range=(min(Eee),max(Eee)), bins=50)
        plt.show()
        #PlotHistogram(Em)
    def DecayTime(self, n, energy):
        pi, mu = [],[]
        for i in xrange(int(n)):
            x = self.sim.ParticleDecayTime(energy)
            if len(x) == 2:
                pi.append(x[0])
                mu.append(x[1])
            elif len(x) == 1:
                pi.append(x[0])
        print "Mean Pion decay time (in lab frame): ",sum(pi)/len(pi)
        print "Mean Muon decay time (in lab frame): ",sum(mu)/len(mu)
        #print sum(pi)*len(mu)/(sum(mu)*len(pi))
        
def main():
    plot = Plot(np.array([[0.1],[0.1],[90]]))
    #PlotExit3D(int(1e4), 1000)
    plot.EnergyDepositedSmart(10000)
    #MuonFraction(1e1, np.logspace(np.log10(500),np.log10(1e4)))
      
if __name__ == '__main__':
    main()    
