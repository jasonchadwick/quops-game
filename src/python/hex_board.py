# Contains functions to represent and manipulate a board of hexagonal tiles.

class SquareHexBoard:
    def __init__(self, size, allow_wrapping):
        #TODO: haven't needed this yet
        pass

"""
Board is organized based on 3 coordinates.
first coordinate increases going down-left
second coordinate increases going down-right
third coordinate increases going straight up

3x3 board:

          (-2, 0, 2)  (-1,-1, 2)  ( 0,-2, 2)


     (-2, 1, 1)  (-1, 0, 1)  ( 0,-1, 1)  ( 1,-2, 1)


(-2, 2, 0)  (-1, 1, 0)  ( 0, 0, 0)  ( 1,-1, 0)  ( 2,-2, 0)


     (-1, 2,-1)  ( 0, 1,-1)  ( 1, 0,-1)  ( 2,-1,-1)
    

          ( 0, 2,-2)  ( 1, 1,-2)  ( 2, 0,-2)

TODO: how to print the hexagon with a point at the top instead?
Harder to do with these coordinates, but definitely possible.
Makes the yin-yang thing look better.

"""
class HexBoard:
    def __init__(self, size, allow_wrapping):
        self.coords_to_idx = {}
        self.idx_to_coords = {}
        counter = 0
        for i in range(size):
            for x in range(-i, i+1):
                for y in range(-i, i+1):
                    for z in range(-i, i+1):
                        if abs(x)+abs(y)+abs(z) == 2*i and x+y+z==0:
                            self.coords_to_idx[(x,y,z)] = counter
                            self.idx_to_coords[counter] = (x,y,z)
                            counter += 1
        self.size = size
        self.wrapping = allow_wrapping
    
    def is_valid_idx(self, idx):
        x,y,z = self.idx_to_coords[idx]
        return self.is_valid_coords((x,y,z))
    
    def is_valid_coords(self, coords):
        x,y,z = coords
        for i in range(self.size):
            if abs(x)+abs(y)+abs(z) == 2*i and x+y+z==0:
                return True
        return False

    def get_adjacent_idxs(self, idx):
        idxs = []
        for coord1 in range(3):
            for coord2 in range(3):
                if coord1 != coord2:
                    coords = list(self.idx_to_coords[idx])
                    coords[coord1] += 1
                    coords[coord2] -= 1
                    if self.is_valid_coords(coords):
                        idxs.append(self.coords_to_idx[tuple(coords)])
                    elif self.wrapping:
                        #TODO: figure out math for this
                        pass
        idxs.sort()
        return idxs

    # printfn is a function that takes in a tile index and returns a 1-line string
    # representation of that tile, preferably the same length regardless of idx.
    def print(self, printfn):
        printlen = len(printfn(0))
        buffer = 2 if printlen % 2 == 0 else 3
        total_len = printlen * (2*self.size-1) + buffer * (2*self.size-2)
        for z in range(-self.size+1, self.size):
            n_vals = 2*self.size - 1 - abs(z)
            cur_len = printlen*n_vals + buffer*(n_vals-1)
            padding = int((total_len - cur_len) / 2)
            print(' ' * padding, end='')
            for n in range(n_vals):
                x = (-(self.size-1) + n) if z >= 0 else -(self.size-1 + z - n)
                y = (self.size-1-z-n) if z >= 0 else (self.size-1-n)
                print(printfn(self.coords_to_idx[(x,y,z)]), end='')
                if n != n_vals-1:
                    print(' ' * buffer, end='')
            print()
        pass

b = HexBoard(3,False)
b.print((lambda x : '{:2}'.format(x)))