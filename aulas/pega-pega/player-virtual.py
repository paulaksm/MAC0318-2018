# Simula virtualmente um robo
from robot import Robot
from tag import TagClient
from random import randint, random
import signal, sys
import math
import time
from numpy.linalg import norm
import numpy as np

rid = randint(100, 1000)
run = False
board = None
tagplayer = -1

client = TagClient('localhost', 10318)
client.info(rid, 14, 19, 7, 13.5)

px, py, course = None, None, None

# Sinal de ctrl-c
def signal_handler(signal, frame):
    client.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

players = {}

while not client.quit:

    # nao recebeu informacoes do campo
    if client.getFieldInfo() is None:
        continue
    elif px is None:
        board = client.getFieldInfo()
        px, py = board[0]*random(), board[1]*random()
        course = math.pi*2.0*random()
        client.setPosition(px, py, course)

    # jogo esta parado
    if client.getStatus() is False:
        players = {}
        continue

    # jogo esta parado
    if client.isPause() is True:
        time.sleep(5)
        client.setPause()

    # nao recebeu informacoes do pegador
    if client.getTagInfo() is None:
        continue

    # verifica se ha posicoes novas
    newposs = client.getPosition()
    for info in newposs:
        posx, posy, course, idd, xsize, ysize, xtag, ytag = info
        if idd != rid:
            players[idd] = [posx, posy]

    tag, interval = client.getTagInfo()  
    pos = [players[p] for p in players]

    if time.time() <= interval:
        # comportamento de fuga
        if tag in players and tag != rid:
            # foge se nao for pegador 
            px = px + (px-players[tag][0])/180.0
            py = py + (py-players[tag][1])/180.0

            course = course+(random()-0.5)/5.0
            client.setPosition(px, py, course)
    else:

        if len(pos) >= 1 and tag == rid:
            move = np.array([px-pos[0][0], py-pos[0][1]])
            move =  move/norm(move)*0.5
            px = px - move[0]
            py = py - move[1]

        if tag != rid:
            px = px+(random()-0.5)
            py = py+(random()-0.5)

        course = course+(random()-0.5)/5.0
        client.setPosition(px, py, course)
