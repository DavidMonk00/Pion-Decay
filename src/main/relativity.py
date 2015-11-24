'''
Created on 17 Nov 2015

@author: david
'''
  
import numpy as np
     
def dot(r1, r2):
    return float(sum(r1*r2))
 
def inner(v1, v2):
    """Inner product of two FourVectors"""
    return v1.temporal()*v2.temporal() - dot(v1.spatial(), v2.spatial())
 
class FourVector:
    """Four-vector class for use in relativity"""
    def __init__(self, temporal = 0, spatial=np.zeros(3).reshape(3,1)):
        self.spatial = np.array(spatial).reshape(3,1)
        self.temporal = temporal
     
    def __str__(self):
        return "(%g, %g, %g, %g)"%(self.temporal,tuple(self.spatial)[0],tuple(self.spatial)[1],tuple(self.spatial)[2])                                    
                                                                                                                 
    def __add__(self, other):
        return FourVector(self.temporal + other.temporal, self.spatial + other.spatial)
     
    def __iadd__(self, other):
        self.temporal += other.temporal
        self.spatial += other.spatial
        return self
     
    def __sub__(self, other):
        return FourVector(self.temporal - other.temporal, self.spatial - other.spatial)
     
    def __isub__(self, other):
        self.temporal -= other.temporal
        self.spatial -= other.spatial
        return self
     
    def magsquare(self):
        return inner(self,self)
         
    def boost(self, beta):
        x,y,z = 0,1,2
        gamma = 1/np.sqrt(1-dot(beta,beta))
        convarr = np.array([[gamma, -gamma*beta[x], -gamma*beta[y], -gamma*beta[z]],
                            [-gamma*beta[x], 1 + (gamma - 1)*(pow(beta[x],2)/dot(beta,beta)), (gamma - 1)*(beta[x]*beta[y]/dot(beta,beta)), (gamma - 1)*(beta[x]*beta[z]/dot(beta,beta))],
                            [-gamma*beta[y], (gamma - 1)*(beta[y]*beta[x]/dot(beta,beta)), 1 + (gamma - 1)*(pow(beta[y],2)/dot(beta,beta)), (gamma - 1)*(beta[y]*beta[z]/dot(beta,beta))],
                            [-gamma*beta[z], (gamma - 1)*(beta[z]*beta[x]/dot(beta,beta)), (gamma - 1)*(beta[z]*beta[y]/dot(beta,beta)), 1 + (gamma - 1)*(pow(beta[z],2)/dot(beta,beta))]])
        vect = np.array([self.temporal]+list(self.spatial)).reshape(4,1)
        b_v = np.dot(convarr,vect)
        return FourVector(float(b_v[0]),b_v[1:])
     
class PositionFourVector(FourVector):
    def __repr__(self):
        return "%s(ct = %g, r = (%g, %g, %g))"%("PositionFourVector",self.temporal,tuple(self.spatial)[0],tuple(self.spatial)[1],tuple(self.spatial)[2])
     
 
class EnergyFourVector(FourVector):
    def __repr__(self):
        return "%s(E/c = %g, p = (%g, %g, %g))"%("EnergyFourVector",self.temporal,tuple(self.spatial)[0],tuple(self.spatial)[1],tuple(self.spatial)[2])

#class VelocityFourVector(FourVector):
#    def __init__(self, initial velcocity):
