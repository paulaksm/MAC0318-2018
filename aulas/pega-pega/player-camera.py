# Simula virtualmente um robo
from robot import Robot
from tag import TagClient
from random import randint, random
import signal, sys
import math
import time

rid = 5
run = False
board = None
tagplayer = -1

client = TagClient('localhost', 10318)
client.info(rid, 10, 10, 5, 5)

px, py, course = None, None, None

# Sinal de ctrl-c
def signal_handler(signal, frame):
    client.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

players = {}

while not client.quit:
    time.sleep(0.1)

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
            # atualiza posicao
            px, py, course = posx, posy, courser

    tag, interval = client.getTagInfo()  
    pos = [players[p] for p in players]

    if time.time() <= interval:
        # comportamento de fuga
        if tag in players and tag != rid:
            # foge se nao for pegador 
            pass
    else:

        if len(pos) >= 1 and tag == rid:
            # acoes caso seja o pegador
            pass

        if tag != rid:
            #acoes de fuga
            pass

