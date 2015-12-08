'''
Created on 17 Nov 2015

@author: david
'''

import numpy as np
from particle import Pion
import constants as constants

class Simulation:
    const = constants.Constants()
    def __init__(self, position):
        self.detector = constants.Detector(position)
    def ParticleExit(self, energy):
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
    def ParticleDetect(self, energy):
        pi = Pion(energy)
        if pi.DecayCheck(np.array([2.5,self.detector.position[2]+0.3])) == False:
            decay_part = pi.Decay()
            if pi.type == 'e':
                return decay_part.EnergyDeposited(self.detector)
            else:
                return 0
                if decay_part.DecayCheck(np.array([2.5,self.detector.position[2]+0.3])) == False:
                    el = decay_part.Decay()
                    return el.EnergyDeposited(self.detector)
                else:
                    return decay_part.EnergyDeposited(self.detector)
        else:
            return 0
    def ParticleEnergy(self, energy):
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
    def ParticleDecay(self, energy):
        pi = Pion(energy)
        decay_positions = []
        if pi.DecayCheck(self.const.dimensions) == False:
            decay_part = pi.Decay()
            decay_positions.append(pi.decay_pos.spatial)
            if pi.type == 'mu':
                if decay_part.DecayCheck(self.const.dimensions) == False:
                    decay_positions.append(decay_part.decay_pos.spatial)
        return decay_positions
    def ParticleDecayTime(self, energy):
        pi = Pion(energy)
        decay_times = []
        pi.DecayCheck(self.const.dimensions)
        decay_part = pi.Decay()
        decay_times.append(pi.decay_time)
        if pi.type == 'mu':
            decay_part.DecayCheck(self.const.dimensions)
            decay_times.append(decay_part.decay_time)
        return decay_times
    def ParticleTranverseMomentum(self, energy):
        pi = Pion(energy)
        if pi.DecayCheck(self.const.dimensions) == False:
            decay_part = pi.Decay()
            if pi.type == 'e':
                return decay_part.energyvector.Transverse()
            else:
                if decay_part.DecayCheck(self.const.dimensions) == False:
                    el = decay_part.Decay()
                    return el.energyvector.Transverse()
                else:
                    return 0
        else:
            return 0
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
