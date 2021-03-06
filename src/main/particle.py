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
    smearing = True
    def __init__(self, energyvector, initial_position, mass = 1, lifetime = 0):
        ''' Initial position is a PostionFourVector class, with t = 0
            energy is a float which is the energy of the particle in MeV'''
        self.energyvector = energyvector
        self.pos = initial_position
        self.mass = mass
        self.gamma = self.energyvector.temporal/mass
        self.beta = energyvector.spatial/(self.gamma*mass)
        self.decay_time = np.random.exponential(self.gamma*lifetime)
    def RecurFocusEnter(self,bool_array):
        l = bool_array.shape[1]
        a = l/2
        for i in xrange(2,int(np.ceil(np.log2(l)))+5):
            p = int(l/2**i)
            if bool_array[:,a].all() != True:
                a += p
            else:
                a -= p
        return a
    def RecurFocusExit(self,bool_array):
        l = bool_array.shape[1]
        a = l/2
        for i in xrange(2,int(np.ceil(np.log2(l)))+5):
            p = int(l/2**i)
            if bool_array[:,a].any() != True:
                a += p
            else:
                a -= p
        return a
    def ExitPosition(self):
        '''
        Calculates where the particle will leave the tube and returns
        this position as an array
        '''
        ct = np.linspace(0,(const.dimensions[1] - self.pos.spatial[2])/self.beta[2],1e4)
        pos = self.pos.spatial +  ct*self.beta
        pos_cyl = np.array([[np.sqrt((pos[0]*pos[0]) + (pos[1]*pos[1]))],[pos[2]]]).reshape(2,pos.shape[1])
        exit_bool = pos_cyl > const.dimensions.reshape(2,1)
        e = self.RecurFocusExit(exit_bool)
        return pos[:,e]
    def Detect(self, detector):
        t_enter = (detector.position-self.pos.spatial)/self.beta
        t_exit = (detector.position+detector.dimensions-self.pos.spatial)/self.beta
        pos_front = self.pos.spatial[:2] + self.beta[:2]*t_enter[2]
        pos_rear = self.pos.spatial[:2] + self.beta[:2]*t_exit[2]
        if (pos_front>detector.position[:2]).all() and (pos_front<(detector.position+detector.dimensions)[:2]).all():
            t = np.sort(np.append(t_exit, t_enter[:2]))
            for i in t:
                if i > t_enter[2]:
                    return np.linalg.norm(self.beta*(t_enter[2]-i))
        elif (pos_rear>detector.position[:2]).all() and (pos_rear<(detector.position+detector.dimensions)[:2]).all():
            t = np.sort(np.append(t_exit[:2], t_enter[:2]))
            for i in xrange(4): 
                if t[i] > t_exit[2]:
                    return np.linalg.norm(self.beta*(t_enter[2]-t[i-1]))
        else:
            return 0
        
class Pion(Particle):
    branching = 1e-4
    def __init__(self, energy, initial_position = rel.PositionFourVector()):
        mass = Mass.pion #in MeV
        lifetime = 2.6e-8
        energyvector = rel.EnergyFourVector(energy,(0,0,np.sqrt(energy*energy - mass*mass)))
        Particle.__init__(self, energyvector, initial_position, mass, lifetime)
    def DecayCheck(self, dimensions):
        '''
        Checks if decay occurs within the tube. 
        Should be called before invoking the Decay() function
        '''
        ct = const.c*self.decay_time
        self.decay_pos = rel.PositionFourVector(self.pos.temporal + ct, ct*self.beta)
        if self.decay_pos.spatial[2] > dimensions[1]:
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
    def EnergyDeposited(self, detector):
        dist = self.Detect(detector)
        E = self.energyvector.temporal*(1 - np.exp(-dist/0.026))
        if E != 0:
            if self.smearing == True:
                smear = np.random.normal(0,0.04)
                return E*(1+smear/np.sqrt(E))
            else:
                return E
        else:
            return 0
    
class Muon(Particle):
    def __init__(self, energyvector, initial_position):
        mass = Mass.muon
        lifetime = 2.2e-6
        Particle.__init__(self, energyvector, initial_position, mass, lifetime)
    def DecayCheck(self, dimensions):
        '''
        Checks if muon decays before leaving the tube. Should be invoked
        before either Decay() or ExitPosition()
        '''
        ct = const.c*self.decay_time
        self.decay_pos = rel.PositionFourVector(self.pos.temporal + ct, ct*self.beta)
        if self.decay_pos.spatial[2] > dimensions[1] or np.sqrt(self.decay_pos.spatial[0]*self.decay_pos.spatial[0] +
                                                                      self.decay_pos.spatial[1]*self.decay_pos.spatial[1]) > dimensions[0]:
            #self.exit_pos = self.ExitPosition()
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
    def EnergyDeposited(self, detector): 
        dist = self.Detect(detector)
        E = 480*dist
        if E != 0:
            if self.smearing == True:
                smear = np.random.normal(0,0.04)
                return E*(1+smear/np.sqrt(E))
            else:
                return E
        else:
            return 0
            
