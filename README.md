# Quops: A board game inspired by quantum mechanics

TODO:
- make this documentation more readable
- work on game balancing (game currently works, but isn't very fun)
- make an android app!

All tiles are entangled - i.e. the entire board is in a superposition of possible
states. These states have different "probability amplitudes" associated with them.
As in quantum mechanics, probability amplitudes are complex numbers. The "expected
value" of a certain board state is calculated by 

An "attack" can be thought of as a CNOT gate - Player 0 attacking a player 1 tile
essentially says "if bit A is in state 0, flip bit B"

IDEA: you can unlock different gate operations
- CNOT
- Cphase?
- SWAP
- etc
IDEA: each player has a "hand" of a few different gates, they can use a couple per turn

Can do 2-3 moves per turn?

Puzzle campaign (build up the possible gates) but also multiplayer

Mathematically, the board is a bit vector [b0, b1, ... bn] and Player 0's goal is to
make the most probable state become [0, 0, ..., 0] while Player 1's goal is to make
it become [1, 1, ..., 1]. This entire game could be described using quantum mechanics
and matrices - the only thing this board design decides is what possible unitary
manipulations are possible on our bits. In a way, you are essentially creating a
quantum computer circuit, step by step (I think this game is Turing complete..?)
So in theory this game could be physically implemented on a quantum computer, with
each tile being a qubit.

What about more than 2 players?
In quantum computing, "qubits" with more than 2 states are known as qudits (for 3-state
systems, they are called qutrits). n qudits that each have d states can represent d^n
total possible "board-states" (ex: 2 qudits of 3 states each can represent the following
8 states: 00, 01, 02, 10, 11, 12, 20, 21, 22)

board indexing (size=3):
```
    13  15  18
  11   4   6  17
 9   2   0   5  16
   8   1   3  14
     7  10  12
```
Organization:
In quantum mechanics terms, the game is in a superposition of 2^ntiles-1 possible states, each of
which has a "probability amplitude" that is related to the probability of that particular
state being observed when the board is "measured". 
Current state of game is stored as a "sparse array"
e.g. if the current state is 1/sqrt(2) (|0000...00> - |1111...11>) then
the state is a list of length 2 containing the tuples (0, 1/sqrt(2)) and (2^n-1, -1/sqrt(2)).
The first number is the state index (which tells us the value of each tile on the board)
and the second number is the probability amplitude, which can be complex.
Operations are essentially unitary matrices on the entire space, but are treated as
a series of conditionals in the code. CNOT(0, 1) is a CNOT gate with the 0 tile as control
and the 1 tile as target. It will search through the game state list, and any tiles that have
the bit patterns |10....> or |11....> will have their amplitudes flipped.
