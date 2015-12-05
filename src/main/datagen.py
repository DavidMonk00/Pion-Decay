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
    def __init__(self, energy):
        self.det = '010190'
        mkdir(self.det)
        self.energy = energy
    def EnergyDepositDumb(self, n, energy, detector):
        sim = Simulation(detector.position)   
        f = open('010190/%s'%energy,'a')
        for i in xrange(long(n)):
            e = sim.ParticleDetect(energy)
            if e != 0:
                e_str = "%.2f"%e
            #if len(e_str) < 6:
            #    e_str = '0' + e_str          
                f.write(e_str+'\n')
        f.close()
    def UploadData(self, energy, detector):
        ftp = FTPExt()
        busy = True
        while busy:
            busy = ftp.BusyCheck()
            if busy == False:
                ftp.UploadData(energy, detector)
                ftp.MakeAvailable()
            else:
                sleep(10)
        ftp.Exit()

def main():
    detector = Detector(np.array([[0.1],[0.1],[90]]))
    #UploadData(0)
    #for i in range(10000):
    #    EnergyDepositDumb(1e5, 10000, detector)

if __name__ == "__main__":
    main()
