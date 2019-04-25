import game

class Lobby():
    players = []
    games = []
    gameCount = 0
    
    def join(self, player):
        self.players.append(player)

    def sendall(self, message):
        for player in self.players:
            player.send(message)

    def disjoin(self, player):
        self.players.remove(player)

    def appendGame(self, game):
        self.games.append(game)
        self.gameCount += 1
        game_ids = []
        for game in self.games:
            game_ids.append(game.id) 
        message = {"action": "gameslist", "games": game_ids}
        self.sendall(message)