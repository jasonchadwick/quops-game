# Quops: A board game inspired by quantum mechanics

Quops (short for "quantum operations" is a board game where the board and cards are based on the rules of quantum mechanics. The goal is 
simple: If you are player 0, get the values of all the tiles as close to 0 as possible. If you are player 1, get them as close to 1 as possible. 

Each player has a hand of 5 cards, some of which affect a single tile and some of which affect two tiles. One-tile cards cannot be played on 
tiles entirely owned by your opponent, and two-tile cards must have one tile that is not completely owned by the opponent. On each turn, a 
player may use up to 3 cards (then they draw back up to 5 at the end of their turn). Play continues until the total sum of all tiles is either 
less than 1 (in which case player 0 has won) or greater than ntiles-1 (in which case player 1 has won).

Tiles are hexagonal (six neighbors), and two-tile cards can only be played on neighboring tiles.

Mathematically, the board is a bit vector [b0, b1, ... bn] and Player 0's goal is to make the most probable state become [0, 0, ..., 0] while 
Player 1's goal is to make it become [1, 1, ..., 1]. This entire game could be described using quantum mechanics and matrices (and it is, in the
code) - the only thing that the hexagonal board design decides is what possible unitary manipulations are allowed on the bits. In a way, you are 
essentially creating a quantum computer circuit, step by step. So in theory this game could be physically implemented on a quantum computer, with 
each tile being a qubit.

### Gameplay

Tile numbering:
```
    13  15  18
  11   4   6  17
 9   2   0   5  16
   8   1   3  14
     7  10  12
```

Gameplay:

```
GAME START
Board:
      0.0   0.0   0.0
   0.0   0.0   0.0   0.0
0.0   0.0   0.5   1.0   1.0
   1.0   1.0   1.0   1.0
      1.0   1.0   1.0
_______________________________________________
Player 0's turn.
Hand:
  0. CNOT 
  1. X 
  2. CH 
  3. SWAP 
  4. H 
Choose a card to play: 0
Target A: 6
Target B: 5
      0.0   0.0   0.0
   0.0   0.0   0.0   0.0
0.0   0.0   0.5   0.0   1.0  <-- tile number 5 was flipped
   1.0   1.0   1.0   1.0
      1.0   1.0   1.0

_______________________________________________
...Player 0 makes 2 more moves...
_______________________________________________
Player 1's turn.
Hand:
  0. CH 
  1. SWAP 
  2. CH 
  3. CNOT 
  4. CNOT 
Choose a card to play: 0
Target A: 8
Target B: 9
                  0.0   0.0   0.0
               0.0   0.0   0.0   0.0
H gate  --> 0.5   0.0   0.5   0.0   1.0
applied to     1.0   1.0   1.0   1.0
                  1.0   1.0   1.0
_______________________________________________
...Player 1 makes 2 more moves...
_______________________________________________
Player 0's turn...
```

### Implementation:

In quantum mechanics terms, the game is in a superposition of 2^ntiles-1 possible states, each of which has a "probability amplitude" that is
related to the probability of that particular state being observed when the board is "measured". Current state of game is stored as a "sparse 
array" e.g. if the current state is 1/sqrt(2) (|0000...00> - |1111...11>) then the state is a list of length 2 containing the tuples (0, 
1/sqrt(2)) and (2^n-1, -1/sqrt(2)). The first number is the state index (which tells us the value of each tile on the board) and the second 
number is the probability amplitude, which can be complex. Operations are essentially unitary matrices on the entire space, but are treated 
as a series of conditionals in the code. CNOT(0, 1) is a CNOT gate with the 0 tile as control and the 1 tile as target. It will search through 
the game state list, and any tiles that have the bit patterns |10....> or |11....> will have their amplitudes flipped.

### Additional physics:

What about more than 2 players?
In quantum computing, "qubits" with more than 2 states are known as qudits (for 3-state
systems, they are called qutrits). n qudits that each have d states can represent d^n
total possible "board-states" (ex: 2 qudits of 3 states each can represent the following
8 states: 00, 01, 02, 10, 11, 12, 20, 21, 22)

### TODO
- win condition = make [0,0,0,...,0] the most probable state
- in-game tutorial/info on each of the cards
- work on game balancing (game currently works, but isn't very fun)
- make an android app!
    - graphics
    - kotlin?
    - online multiplayer
- puzzle campaign (build up the possible gates)
- AI offline opponent
