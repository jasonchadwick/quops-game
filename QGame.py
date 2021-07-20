from Board import *
from Player import *

class QGame():
    def __init__(self, size=3, handsize=5, ops_per_turn=3, win_threshold=0.9):
        self.board = Board(size)
        self.score = 0
        self.params = {"handsize" : 5,
                       "ops_per_turn" : 3,
                       "win_threshold" : 0.9}
        self.player0 = Player(0, handsize)
        self.player1 = Player(1, handsize)
        self.deck = self.populate_deck()
    
    def populate_deck(self, preset=None):
        # TODO
        # make a deck of allowed gates that players draw their hand from
        pass

    def calc_score(self):
        # if sum of tiles is 0, player 0 wins, if 1 then player 1 wins
        expected_vals = self.board.calc_expect()
        p1_score = sum(expected_vals) / self.board.ntiles
        p2_score = 1 - p1_score
        return (p1_score, p2_score)

    def measure(self):
        # TODO
        # measures the board, picking a single possible state
        # TODO: can players do this during the game?
        pass

    def do_turn(self, player):
        # TODO
        # one player does a turn (uses `ops_per_turn` number of gates on the board)
        pass

    def play(self):
        # TODO
        # loop of player turns until there is a winner
        pass