'''
Created on 17 Nov 2015

@author: david
'''

import numpy as np
import relativity as rel
import constants as constants

const = constants.Constants()
Mass = constants.Mass()

def Michel():
    '''Generates triangular distribution'''
    x, y = np.random.random(2)
    if x >= y:
        return 0.25 + x * 52.75
    else:
        return 0.25 + y * 52.75

class Particle:
    '''
    Base particle class: __init__ calculates beta, gamma and decay time for given particle
    '''
    def __init__(self, energyvector, initial_position, mass = 1, lifetime = 0):
        ''' Initial position is a PostionFourVector class, with t = 0
            energy is a float which is the energy of the particle in MeV'''
        self.energyvector = energyvector
        self.pos = initial_position
        self.mass = mass
        self.gamma = self.energyvector.temporal/mass
        self.beta = energyvector.spatial/(self.gamma*mass)
        self.decay_time = np.random.exponential(self.gamma*lifetime)
    def ExitPosition(self):
        '''
        Calculates where the particle will leave the tube and returns
        this position as an array
        '''
        ct = np.linspace(0,(const.dimensions[1] - self.pos.spatial[2])/self.beta[2],1e3)
        pos = self.pos.spatial +  ct*self.beta
        pos_cyl = np.array([[np.sqrt((pos[0]*pos[0]) + (pos[1]*pos[1]))],[pos[2]]]).reshape(2,pos.shape[1])
        exit_bool = pos_cyl < const.dimensions.reshape(2,1)
        a = exit_bool.shape[1]/2
        for i in range(2,int(np.ceil(np.log2(exit_bool.shape[1])))):
            p = int(exit_bool.shape[1]/2**i)
            if exit_bool[:,a].all() != True:
                a -= p
            else:
                a += p
        return pos[:,a]
        
class Pion(Particle):
    branching = 1e-4
    def __init__(self, energy, initial_position = rel.PositionFourVector()):
        mass = Mass.pion #in MeV
        lifetime = 2.6e-8
        energyvector = rel.EnergyFourVector(energy,(0,0,np.sqrt(energy*energy - mass*mass)))
        Particle.__init__(self, energyvector, initial_position, mass, lifetime)
    def DecayCheck(self):
        '''
        Checks if decay occurs within the tube. 
        Should be called before invoking the Decay() function
        '''
        ct = const.c*self.decay_time
        self.decay_pos = rel.PositionFourVector(self.pos.temporal + ct, ct*self.beta)
        if self.decay_pos.spatial[2] > 100:
            self.type = "e"
            self.exit_pos = np.array([0,0,100])
            return True
        return False
    def Decay(self):
        '''
        Decays particle into either an electron or muon, and returns their
        class with initial position and energy.
        '''
        _phi = 2*np.pi*np.random.uniform()
        _costheta = 2*np.random.uniform() - 1
        _theta = np.arccos(_costheta)
        if np.random.uniform() < self.branching:
            self.type = "e"
            energy = (self.mass*self.mass + Mass.electron*Mass.electron)/(2*self.mass) #Neutrino mass is neglected
            p = np.sqrt(energy*energy - Mass.electron*Mass.electron)
            return Electron(rel.EnergyFourVector(energy,(p*np.sin(_theta)*np.cos(_phi),
                                                         p*np.sin(_theta)*np.sin(_phi),
                                                         p*_costheta)).boost(-self.beta),
                            self.decay_pos)
        else:
            self.type = "mu"
            energy = (self.mass*self.mass + Mass.muon*Mass.muon)/(2*self.mass) #Neutrino mass is neglected
            p = np.sqrt(energy*energy - Mass.muon*Mass.muon)
            return Muon(rel.EnergyFourVector(energy,(p*np.sin(_theta)*np.cos(_phi),
                                                         p*np.sin(_theta)*np.sin(_phi),
                                                         p*_costheta)).boost(-self.beta),
                        self.decay_pos) 

class Electron(Particle):
    def __init__(self, energyvector, initial_position):
        mass = Mass.electron #in MeV
        lifetime = np.Inf
        Particle.__init__(self, energyvector, initial_position, mass, lifetime)   
    

class Muon(Particle):
    def __init__(self, energyvector, initial_position):
        mass = Mass.muon
        lifetime = 2.2e-6
        Particle.__init__(self, energyvector, initial_position, mass, lifetime)
    def DecayCheck(self):
        '''
        Checks if muon decays before leaving the tube. Should be invoked
        before either Decay() or ExitPosition()
        '''
        ct = const.c*self.decay_time
        self.decay_pos = rel.PositionFourVector(self.pos.temporal + ct, ct*self.beta)
        if self.decay_pos.spatial[2] > const.dimensions[1] or np.sqrt(self.decay_pos.spatial[0]*self.decay_pos.spatial[0] +
                                                                      self.decay_pos.spatial[1]*self.decay_pos.spatial[1]) > const.dimensions[0]:
            self.exit_pos = self.ExitPosition()
            return True
        return False   
    def Decay(self):
        '''
        Decays muon into electron and returns an electron class with
        initial position and energy
        '''
        _phi = 2*np.pi*np.random.uniform()
        _costheta = 2*np.random.uniform() - 1
        _theta = np.arccos(_costheta)
        energy = Michel()
        p = np.sqrt(energy*energy - Mass.electron*Mass.electron)
        return Electron(rel.EnergyFourVector(energy,(p*np.sin(_theta)*np.cos(_phi),
                                                         p*np.sin(_theta)*np.sin(_phi),
                                                         p*_costheta)).boost(-self.beta),
                        self.decay_pos)
