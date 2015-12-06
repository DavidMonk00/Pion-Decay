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
        #mkdir(self.det)
        self.energy = energy
    def EnergyDepositDumb(self, n, detector):
        sim = Simulation(detector.position)   
        f = open('010190/%s.data'%self.energy,'w')
        fb = open('010190/%s.databackup'%self.energy,'a')
        for i in xrange(long(n)):
            e = sim.ParticleDetect(self.energy)
            if e != 0:
                e_str = "%.2f"%e
            #if len(e_str) < 6:
            #    e_str = '0' + e_str          
                f.write(e_str+'\n')
                fb.write(e_str+'\n')
        f.close()
        fb.close()
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
    x = Gen(1000)
    for i in range(10):
        x.EnergyDepositDumb(10000, detector)
        x.UploadData()

if __name__ == "__main__":
    main()
