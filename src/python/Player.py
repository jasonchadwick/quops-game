class Player():
    def __init__(self, playernum, drawfunc, handsize=5):
        self.playernum = playernum
        self.drawfunc = drawfunc
        self.handsize = handsize
        self.hand = []
    
    def fillhand(self):
        while len(self.hand) < self.handsize:
            self.hand.append(self.drawfunc())

    def printdeck(self):
        for i,card in enumerate(self.hand):
            print("  " + str(i) + ". ", end='')
            card.print()
            print()