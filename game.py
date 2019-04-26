import random

class Game():
    def __init__(self, id, player):
        self.boxes = []
        self.players = []
        self.isStarted = False
        self.id = id
        self.join(player)
        self.owner = player
        self.createBoxes()

    def join(self, player):
        player.score = 0
        self.players.append(player)
        player.game = self
        message = {"action": "gamejoined"}
        player.send(message)

    def createBoxes(self):
        for i in range(20):
            self.boxes.append({"x": random.randint(0, 640), "y": random.randint(0, 640)})

    def start(self):
        message = '{"action": "gamestart"}' #client aldiginda oyun 5 saniye icinde baslar
        self.update()
        self.sendall(message)
        self.isStarted = True

    def sendall(self, message):
        for player in self.players:
            player.send(message)

    def checkBox(self, boxx, boxy, x, y):
        boxsize = 30
        return (x > boxx - boxsize) and (x < boxx + boxsize) and (y > boxy - boxsize) and (y < boxy + boxsize)
    
    def click(self, player, x, y):
        for box in self.boxes:
            if self.checkBox(box["x"], box["y"], x, y):
                self.boxes.remove(box)
                player.score += 1
                break
        self.update()

    def getScores(self):
        scores = []
        for p in self.players:
            scores.append({p.nickname: p.score})
        return scores

    def playerQuit(self, player):
        if self.owner == player:
            self.gameEnd()        
        else:
            self.players.remove(player)

    def gameEnd(self):
        self.isStarted = False
        message = {"action": "gameend"}
        self.sendall(message)
        for p in self.players:
            p.game = None
        self.owner.lobby.removeGame(self)
        
    def update(self):
        message = {"action": "update"}
        message["boxes"] = self.boxes
        message["scores"] = self.getScores()
        self.sendall(message)
        if (len(self.boxes) == 0):
            self.gameEnd()
        