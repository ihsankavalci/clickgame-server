import room
import game
import json
class Player():
    def __init__(self, socket, id, lobby):
        self.socket = socket
        self.id = id
        self.lobby = lobby
        self.game = None
        
    def setNickname(self, nickname):
        self.nickname = nickname
        message = {"action": "playerconnected", "nickname": nickname}
        self.lobby.sendall(message)

    def send(self, message):
        if type(message) is dict:
            message = json.dumps(message)
        self.socket.send(message.encode('ascii'))

    def sendChat(self, msg):
        message = '{"action": "chat", "msg": "%s: %s"}' % (self.nickname, msg)
        self.lobby.sendall(message)
    
    def disconnect(self):
        self.lobby.disjoin(self)
        del self

    def createGame(self):
        g = game.Game(self.lobby.gameCount)
        g.join(self)
        self.lobby.appendGame(g)
    
    def joinGame(self, gameid):
        for g in self.lobby.games:
            if (g.id == gameid):
                g.join(self)
                break