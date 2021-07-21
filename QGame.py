from Board import *
from Player import *
from Card import *

class QGame():
    def __init__(self, size=3, handsize=5, ops_per_turn=3, win_threshold=None):
        self.board = Board(size)
        if win_threshold is None:
            win_threshold = 1/self.board.ntiles
        self.params = {"handsize" : handsize,
                       "ops_per_turn" : ops_per_turn,
                       "win_threshold" : win_threshold}
        self.player0 = Player(0, self.drawcard, handsize)
        self.player1 = Player(1, self.drawcard, handsize)

    def drawcard(self):
        cards = [Card(name,gate) for name,gate in [("X",X), ("H",H), ("SWAP",SWAP), ("CNOT",CNOT), ("CH",CH), ("RXX.pi/2",RXX(np.pi/2))]]
        p = [0.1, 0.2, 0.2, 0.2, 0.2, 0.1]
        return np.random.choice(cards, p=p)

    def check_winner(self):
        expected_vals = self.board.calc_expect()
        score = sum(expected_vals) / self.board.ntiles
        if score < self.params["win_threshold"]:
            return 0
        elif 1-score < self.params["win_threshold"]:
            return 1
        else:
            return None

    def measure(self):
        # TODO
        # measures the board, picking a single possible state
        # TODO: can players do this during the game?
        pass

    def do_turn(self, player):
        # one player does a turn (uses `ops_per_turn` number of gates on the board)
        class InvalidMove(Exception):
            pass

        invalidmove = InvalidMove()
        player.fillhand()
        print("_______________________________________________")
        print("Player " + str(player.playernum) + "'s turn.")
        i = 0
        while i < self.params["ops_per_turn"]:
            try:
                print("Deck:")
                player.printdeck()
                card_idx = int(input("Choose a card to play: "))
                card = player.hand[card_idx]
                if card.nbits == 1:
                    tgt = int(input("Target tile: "))
                    # not allowed on pieces entirely owned by opponent
                    if abs(self.board.calc_expect()[tgt] - (1-player.playernum)) < 1e-15:
                        raise invalidmove
                    self.board.onebitgate(tgt, card.gate)
                elif card.nbits == 2:
                    tgtA = int(input("Target A: "))
                    tgtB = int(input("Target B: "))
                    # not allowed to control on pieces entirely owned by opponent
                    if abs(self.board.calc_expect()[tgtA] - (1-player.playernum)) < 1e-15:
                        raise invalidmove
                    res = self.board.twobitgate(tgtA, tgtB, card.gate, invert=(player.playernum==0))
                    if res == False: # invalid operation
                        raise invalidmove

                player.hand.remove(card)
            except InvalidMove:
                print()
                print("Invalid Move. Try again:")
                continue
            i += 1

    def play(self):
        winner = None
        while winner is None:
            self.print()
            self.do_turn(self.player0)
            winner = self.check_winner()
            self.print()
            self.do_turn(self.player1)
            winner = self.check_winner()
        print("Player " + str(winner) + " wins!!!")
        return 0
    
    def print(self):
        self.board.print()

g = QGame(ops_per_turn=2)
g.play()