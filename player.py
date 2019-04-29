import game
import json
class Player():
    def __init__(self, socket, lobby):
        lobby.lock.acquire()
        self.socket = socket
        self.id = lobby.playerIndex
        lobby.playerIndex += 1
        self.lobby = lobby
        self.game = None
        self.nickname = "player%d" % self.id
        lobby.lock.release()
        
    def setNickname(self, nickname):
        self.lobby.lock.acquire()
        self.nickname = nickname
        self.lobby.updatePlayerList()
        self.lobby.lock.release()

    def send(self, message):
        self.lobby.lock.acquire()
        if type(message) is dict:
            message = json.dumps(message)
        
        message += '\n' # temp for client
        try:
            self.socket.send(message.encode('ascii'))
        except Exception as e:
            print('ExceptionSend', e) 
        self.lobby.lock.release()

    def sendChat(self, msg):
        self.lobby.lock.acquire()
        message = {"action": "chat", "msg": "%s -  %s" % (self.nickname, msg)}
        self.lobby.sendall(message)
        self.lobby.lock.release()
    
    def disconnect(self):
        self.lobby.lock.acquire()
        self.lobby.disjoin(self)
        self.lobby.lock.release()
        del self
        

    def createGame(self):
        self.lobby.lock.acquire()
        g = game.Game(self.lobby.gameIndex, self)
        self.lobby.appendGame(g)
        self.lobby.lock.release()
    
    def joinGame(self, gameid):
        self.lobby.lock.acquire()
        for g in self.lobby.games:
            if (g.id == gameid):
                g.join(self)
                break
        self.lobby.lock.release()