import numpy as np

class Card:
    def __init__(self, name, gate, nbits=None):
        self.name = name
        self.gate = gate
        if nbits == None:
            self.nbits = int(np.log2(len(gate)))
        else:
            self.nbits = nbits
    
    def print(self):
        print(self.name + " ", end='')