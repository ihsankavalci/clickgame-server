import random

class Game():
    boxes = []
    players = []
    isStarted = False
    def __init__(self, id):
        self.id = id
        self.createBoxes()
    def join(self, player):
        player.score = 0
        self.players.append(player)
        player.game = self
    def createBoxes(self):
        for i in range(10):
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
        if (x > boxx - boxsize) and (x < boxx + boxsize) and (y > boxy - boxsize) and (y < boxy + boxsize):
            return True
    
    def click(self, player, x, y):
        for box in self.boxes:
            if self.checkBox(box["x"], box["y"], x, y):
                self.boxes.remove(box)
                player.score += 1
                self.update()
                return
    def update(self):
        message = {"action": "update"}
        message["boxes"] = self.boxes
        self.sendall(message)
        