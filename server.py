import socket 

import _thread
import threading 
import json
import player
from lobby import Lobby

lobby = Lobby()

def get_message(data, length):
    return json.loads(data[:length])

def process_raw_packet(packet, rest):
    messages = []
    totalLength = len(packet)

    if (len(rest) > 0):
        packet = rest + packet
    
    index = 0
    while (index < totalLength):
        if (totalLength - index < 4):
            rest = packet[index:]
            return (messages, rest)
        
        length = int.from_bytes(packet[index:index+4], byteorder='little')
        if (length + 4 > (totalLength - index)):
            rest = packet[index:]
            return (messages, rest)
        else:
            messages.append(get_message(packet[index+4:], length))
            index += length+4
            rest = b''
    
    return (messages, rest)

def client_thread(c):
    print(c)
    p = player.Player(c, lobby)
    lobby.join(p)
    theRest = b''

    while True: 
        try:
            data = c.recv(1024)
        except Exception as e:
            print('Exception', e) 
            break

        messages, theRest = process_raw_packet(data, theRest)
        print(p.nickname, messages)
        for message in messages:
            if (message["action"] == "setnickname"):
                p.setNickname(message["nickname"])
            elif (message["action"] == "creategame"):
                p.createGame()
            elif (message["action"] == "joingame"):
                p.joinGame(message["gameid"])
            elif (message["action"] == "startgame"):
                if (p.game != None):
                    p.game.start()
                else:
                    p.send({"action":"nogame"})    
            elif (message["action"] == "click"):
                if (p.game != None):
                    if (p.game.isStarted):
                        p.game.click(p, message["x"], message["y"])
                else:
                    p.send({"action":"nogame"})
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
        c.settimeout(360)
        print('Connected to :', addr[0], ':', addr[1]) 
        _thread.start_new_thread(client_thread, (c,))

    print("exit")
    s.close() 