import game

class Room():
    players = []

    def join(self, player):
        self.players.append(player)
    
    def startGame(self):
        self.game = game.Game()
    