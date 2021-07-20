import numpy as np
from scipy import linalg

class Gate:
    def __init__(self, nbits, gatemat):
        self.nbits = nbits
        self.gatemat = gatemat
        # TODO: finish this class and convert gates to this class

CNOT = np.array([[1,0,0,0],
                 [0,1,0,0],
                 [0,0,0,1],
                 [0,0,1,0]])

X = np.array([[0, 1],
              [1, 0]])

Y = np.array([[0, -1j],
              [1j, 0]])

Z = np.array([[1, 0],
              [0, -1]])

h = 1/np.sqrt(2)

H = np.array([[h,  h],
              [h, -h]])

def RX(theta):
    return linalg.expm(-theta/2*1j*X)

def RY(theta):
    return linalg.expm(-theta/2*1j*Y)

def RZ(theta):
    return linalg.expm(-theta/2*1j*Z)

def RXX(theta):
    return linalg.expm(-theta/2*1j*np.kron(X,X))

def RYY(theta):
    return linalg.expm(-theta/2*1j*np.kron(Y,Y))

def RZZ(theta):
    return linalg.expm(-theta/2*1j*np.kron(Z,Z))