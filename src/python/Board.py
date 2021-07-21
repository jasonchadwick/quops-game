import numpy as np
from gates import *
from game_utils.hex_board import HexBoard

np.set_printoptions(precision=3)

class Board(HexBoard):
    def __init__(self, size):
        super().__init__(size, False)
        self.ntiles = 1 + 6*(sum(range(size)))
        self.nrows = 1 + 4*(size-1)
        self.make_starting_states()
    
    def make_starting_states(self):
        # tile 0 (middle tile) is 50% chance 0 or 1
        state1 = np.zeros(self.ntiles, int)
        state1[0] = 0
        state2 = np.zeros(self.ntiles, int)
        state2[0] = 1
        for z in range(-self.size+1, self.size):
            if z < 0:
                for x in range(-self.size+1-z, self.size-1):
                    y = -x-z
                    state1[self.coords_to_idx[(x,y,z)]] = 0
                    state2[self.coords_to_idx[(x,y,z)]] = 0
            elif z == 0:
                for x in range(-self.size+1, self.size):
                    y = -x
                    if x < 0:
                        state1[self.coords_to_idx[(x,y,z)]] = 0
                        state2[self.coords_to_idx[(x,y,z)]] = 0
                    elif x > 0:
                        state1[self.coords_to_idx[(x,y,z)]] = 1
                        state2[self.coords_to_idx[(x,y,z)]] = 1
            else:
                for x in range(-self.size+1, self.size-z):
                    y = -x-z
                    state1[self.coords_to_idx[(x,y,z)]] = 1
                    state2[self.coords_to_idx[(x,y,z)]] = 1
        self.states = {self.state_idx_from_bits(state1): 1/np.sqrt(2),
                       self.state_idx_from_bits(state2): 1/np.sqrt(2)}

    def state_idx_from_bits(self, bits):
        result = 0
        for i,b in enumerate(bits):
            result += b*2**i
        return int(result)
    
    def bits_from_state_idx(self, idx):
        bits = np.zeros(self.ntiles, int)
        for i in range(self.ntiles-1, -1, -1):
            if idx >= 2**i:
                bits[i] = 1
                idx -= 2**i
        return bits

    def popstate(self, idx):
        self.states.pop(idx)

    def addstate(self, idx, amp):
        if amp == 0:
            return
        if idx in self.states:
            self.states[idx] += amp
        else:
            self.states[idx] = amp

    def prunestates(self):
        states_to_rm = []
        for idx in self.states:
            amp = self.states[idx]
            if abs(amp) < 1e-15:
                states_to_rm.append(idx)
        for idx in states_to_rm:
            self.popstate(idx)

    def onebitgate(self, target, gate):
        # TODO: use gate class instead of matrices
        states_to_rm = []
        states_to_add = []
        for idx in self.states:
            bits = self.bits_from_state_idx(idx)
            amp = self.states[idx]
            bit = bits[target]
            newbits0 = np.concatenate((bits[:target], [0], bits[target+1:]))
            amp0 = gate[0,bit] * amp
            newbits1 = np.concatenate((bits[:target], [1], bits[target+1:]))
            amp1 = gate[1,bit] * amp
            states_to_rm.append(idx)
            states_to_add.append((self.state_idx_from_bits(newbits0), amp0))
            states_to_add.append((self.state_idx_from_bits(newbits1), amp1))
        for idx in states_to_rm:
            self.popstate(idx)
        for (idx,amp) in states_to_add:
            self.addstate(idx,amp)
        self.prunestates()

    def twobitgate(self, tgtA, tgtB, gate, invert=False):
        # return False if invalid gate, else True
        if invert:
            gatenew = np.zeros((4,4),dtype=np.complex64)
            for i in range(4):
                for j in range(4):
                    gatenew[i,j] = gate[(i+2) % 4, (j+2) % 4]
            gate = gatenew
        if tgtB not in self.get_adjacent_idxs(tgtA):
            return False
        states_to_rm = []
        states_to_add = []
        for idx in self.states:
            bits = self.bits_from_state_idx(idx)
            amp = self.states[idx]
            bitA = bits[tgtA]
            bitB = bits[tgtB]
            for newA,newB in [[0,0],[0,1],[1,0],[1,1]]:
                newamp = gate[2*newA+newB, 2*bitA+bitB] * amp
                if tgtA <= tgtB:
                    newbits = np.concatenate((bits[:tgtA], [newA], bits[tgtA+1:tgtB], [newB], bits[tgtB+1:]))
                else:
                    newbits = np.concatenate((bits[:tgtB], [newB], bits[tgtB+1:tgtA], [newA], bits[tgtA+1:]))
                states_to_add.append((self.state_idx_from_bits(newbits), newamp))
            states_to_rm.append(idx)
        for idx in states_to_rm:
            self.popstate(idx)
        for (idx,amp) in states_to_add:
            self.addstate(idx,amp)
        self.prunestates()
        return True
    
    def calc_expect(self):
        expected_vals = np.zeros(self.ntiles)
        for idx in self.states:
            p = abs(self.states[idx])**2
            bits = self.bits_from_state_idx(idx)
            for i in range(self.ntiles):
                if bits[i] == 1:
                    expected_vals[i] += p
        return expected_vals

    def print(self):
        expected_vals = self.calc_expect()
        super().print((lambda i : '{:.3}'.format(expected_vals[i])))