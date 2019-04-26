import game
import threading
class Lobby():
    def __init__(self):
        self.players = []
        self.playerIndex = 0
        self.games = []
        self.gameIndex = 0
        self.lock = threading.RLock()

    def join(self, player):
        self.lock.acquire()
        self.players.append(player)
        self.updatePlayerList()
        self.sendGamesList(player)
        self.lock.release()

    def disjoin(self, player):
        self.players.remove(player)
        if player.game != None:
            player.game.playerQuit(player)
        self.updatePlayerList()

    def removeGame(self, game):
        self.games.remove(game)
        del game

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