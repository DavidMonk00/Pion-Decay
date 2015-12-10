'''
Created on 3 Dec 2015

@author: david
'''

from sim import Simulation
import numpy as np
from constants import Detector
from ftp import FTPExt
from time import sleep
from os import mkdir

class Gen:
    '''Class for data generation and uploading to FTP server. 
    Takes the argument of the initial energy of the Pion.'''
    def __init__(self, energy):
        self.det = '010190'
        #mkdir(self.det)
        self.energy = energy
    def EnergyDepositDumb(self, n, detector):
        sim = Simulation(detector.position)   
        f = open('01-0190/%s'%self.energy,'w')
        for i in xrange(long(n)):
            e = sim.ParticleDetect(self.energy)
            if e != 0:
                #f.write(e_str+'\n')
                fb.write(str(e)+'\n')
        #f.close()
        fb.close()
    def TransverseMomentum(self, n, detector):
        sim = Simulation(detector.position)
        f = open('%s_tp.data'%self.energy,'a')
        for i in xrange(long(n)):
            p = sim.ParticleTranverseMomentum(self.energy)
            if p != 0:
                f.write(str(p)+'\n')
    def UploadData(self):
        ftp = FTPExt()
        busy = True
        while busy:
            busy = ftp.BusyCheck()
            if busy == False:
                ftp.UploadData(self.energy, self.det)
                ftp.MakeAvailable()
            else:
                sleep(10)
        ftp.Exit()

def main():
    detector = Detector(np.array([[0.1],[0.1],[90]]))
    x = Gen(10000)
    cpus = 1
    iterations =  1e5
    loops = iterations/(cpus*10000)
    for i in xrange(int(loops)):
        print "%s%%"%(float(i)/loops*100)
        x.EnergyDepositDumb(10000, detector)
        #x.TransverseMomentum(10000, detector)
        #x.UploadData()

if __name__ == "__main__":
    main()
