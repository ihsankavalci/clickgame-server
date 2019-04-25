    def sendall(self, message):
        for player in self.players:
            player.socket.send(message.encode('ascii'))