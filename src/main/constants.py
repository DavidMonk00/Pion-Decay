'''
Created on 17 Nov 2015

@author: david
'''

from numpy import array,ones

class Constants:
    '''
    A class of fundamental physical constants
    '''
    c = 3e8
    e = 1.6e-19
    dimensions = array([[2.5],[100]])

class Detector:
    def __init__(self, position):
        self.position = position #Bottom front left of detector
    dimensions = ones(3).reshape(3,1)*0.3
    
class Mass:
    electron = 0.5
    pion = 139.6
    muon = 105.7
