import bluetooth
from robot import Robot
from tag import TagClient
from random import randint, random
import signal, sys
import math
import time
import numpy as np

serverMACAddress = '00:16:53:18:2E:17'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))

#while 1:
#    text = bytes([1])
#    if text == "quit":
#        break
#    s.send(bytes([1]))
#sock.close()


rid = 11
run = False
board = None
tagplayer = -1

client = TagClient('localhost', 10318)
client.info(rid, 14, 19, 7, 13.5)

px, py, course = None, None, None

# Sinal de ctrl-c
def signal_handler(signal, frame):
    client.stop()
    sock.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

players = {}

while not client.quit:
    time.sleep(0.4)

    # nao recebeu informacoes do campo
    if client.getFieldInfo() is None:
        continue
    elif px is None:
        board = client.getFieldInfo()
        px, py = board[0]*random(), board[1]*random()
        course = math.pi*2.0*random()

    # jogo esta pausado
    if client.getStatus() is False:
        players = {}
        s.send(bytes([0x65]))
        continue

    # nao recebeu informacoes do pegador
    if client.getTagInfo() is None:
        continue

    # verifica se ha posicoes novas
    newposs = client.getPosition()
    for info in newposs:
        posx, posy, courser, idd, xsize, ysize, xtag, ytag = info
        if idd != rid:
            players[idd] = [posx, posy]
        else:
            px, py, course = posx, posy, courser

    tag, interval = client.getTagInfo()  
    pos = [players[p] for p in players]

    x1, y1 = 0, 0
    if time.time() >= interval and len(pos) >= 1 and tag == rid:
        print("Pegando")
        x1 = -py+pos[0][1]
        y1 = -px+pos[0][0]
    elif tag != rid:
        print("Fugindo")
        x1 = py-players[tag][1]
        y1 = px-players[tag][0]

    else:
        print("Esperando")
        s.send(bytes([5]))
        continue
    x2 = math.cos(course)
    y2 = math.sin(course)

    u = np.array([-x1, y1])
    v = np.array([x2, -y2])
    angle = np.math.atan2(np.linalg.det([u,v]),np.dot(u,v))

    print([u,v], angle)

    if abs(angle) < 0.2:
        s.send(bytes([1]))
    elif angle < 0:
        s.send(bytes([4]))
    else:
        s.send(bytes([3]))

s.send(bytes([0x65]))
s.send(bytes([0x64]))

