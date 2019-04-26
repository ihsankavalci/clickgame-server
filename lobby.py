import game
class Lobby():
    def __init__(self):
        self.players = []
        self.playerIndex = 0
        self.games = []
        self.gameIndex = 0

    def join(self, player):
        self.players.append(player)
        self.updatePlayerList()
        self.sendGamesList(player)

    def disjoin(self, player):
        self.players.remove(player)
        self.updatePlayerList()

    def updatePlayerList(self):
        players_nicknames = []
        for p in self.players:
            players_nicknames.append(p.nickname) 
        message = {"action": "playerlist", "players": players_nicknames}
        self.sendall(message)

    def sendall(self, message):
        for player in self.players:
            player.send(message)

    def sendGamesList(self, player):
        game_ids = []
        for game in self.games:
            game_ids.append(game.id) 
        message = {"action": "gameslist", "games": game_ids}
        player.send(message)

    def appendGame(self, game):
        self.games.append(game)
        self.gameIndex += 1
        game_ids = []
        for game in self.games:
            game_ids.append(game.id) 
        message = {"action": "gameslist", "games": game_ids}
        self.sendall(message)