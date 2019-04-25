import socket 

import _thread
import threading 
import json
import player
from lobby import Lobby

lobby = Lobby()

def client_thread(c):
    print(c)
    p = player.Player(c, lobby)
    lobby.join(p)
    while True: 
        try:
            data = c.recv(1024)
        except Exception as e:
            print('Exception', e) 
            break
        print(data)
        messages = []
        for line in data.splitlines():
            messages.append(json.loads(line))

        for message in messages:
            if (message["action"] == "setnickname"):
                p.setNickname(message["nickname"])
            elif (message["action"] == "creategame"):
                p.createGame()
            elif (message["action"] == "joingame"):
                p.joinGame(message["gameid"])
            elif (message["action"] == "startgame"):
                try:
                    p.game
                    p.game.start()
                except:
                    p.send("nogame")
                
            elif (message["action"] == "click"):
                try:
                    p.game
                    if (p.game.isStarted):
                        p.game.click(x, y)
                except:
                    p.send("nogame")
            elif (message["action"] == "chat"):
                p.sendChat(message["msg"])
        
        if not data: 
            break
        
    print('Bye') 
    p.disconnect()
    c.close() 

if __name__ == "__main__":
    host = "" 
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("Binded to port ", port) 
    s.listen(5) 
    while True: 
        c, addr = s.accept() 
        c.setblocking(0)
        c.settimeout(120)
        print('Connected to :', addr[0], ':', addr[1]) 
        _thread.start_new_thread(client_thread, (c,))

    print("exit")
    s.close() 