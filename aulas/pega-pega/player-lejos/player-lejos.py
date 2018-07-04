import bluetooth
from robot import Robot
from tag import TagClient
from random import randint, random, choice
import signal, sys
import math
import time
import numpy as np

# 001653182E17
serverMACAddress = '00:16:53:18:2E:17' 
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))

rid = 11
run = False
board = None
tagplayer = -1

client = TagClient('192.168.0.101', 10318)
client.info(rid, 14, 19, 7, 13.5)

px, py, course = None, None, None

# Sinal de ctrl-c
def signal_handler(signal, frame):
    client.stop()
    sock.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

players = {}

behaviour = [-0.1, -3, 5]
beha_dict = {-0.1: 'forward', -3:'left', 5:'right'}

while not client.quit:

    # nao recebeu informacoes do campo
    if client.getFieldInfo() is None:
        continue
    elif px is None and py is None:
        board = client.getFieldInfo()

    # # mostra o campo potencial
    maplines = client.getMapLines()

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
        posx, posy, courser, idd, xsize, ysize, xtag, ytag = info
        if idd != rid:
            players[idd] = [posx, posy]
        else:
            px, py, course = posx, posy, courser

    tag, interval = client.getTagInfo()  

    objectives, dangers = [], []
    stoped = False

    if time.time() <= interval:
        # comportamento de fuga
        if tag in players and tag != rid:
            # foge se nao for pegador 
            dangers.append(players[tag])
        else:
            # fica parado
            stoped = True
    else:

        if len(players) >= 1 and tag == rid:
            # pega
            for i in players:
                if players[i] != rid:
                    objectives.append(players[i])

        if tag != rid:
            # foge
            dangers.append(players[tag])

    angle = choice(behaviour)
    print('Command {}:'.format(beha_dict.get(angle)))
    if not stoped:
        if abs(angle) < 0.2:
            s.send(bytes([1])) # forward
        elif angle < 0:
            s.send(bytes([4])) # left
        else:
            s.send(bytes([3])) # right

s.send(bytes([0x65]))
s.send(bytes([0x64])) # encerra a aplicacao
