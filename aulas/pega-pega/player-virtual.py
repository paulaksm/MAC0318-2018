# Simula virtualmente um robo
from robot import Robot
from tag import TagClient
from random import randint, random
import signal, sys
import math
import time
from numpy.linalg import norm
import numpy as np
from potential_fields import potencial
import cv2


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
    elif px is None and py is None:
        board = client.getFieldInfo()
        # posicao inicial
        px, py = 100+random()*100, 50+random()*50 # posicao aleatoria por estar no virtual
        course = math.pi*2.0*random() # virtual robot heading direction
        client.setPosition(px, py, course)

    # # mostra o campo potencial
    maplines = client.getMapLines() # retorna todas as linhas dos obstaculos...as linhas sao informadas no servidor (main.py)

    # jogo esta parado
    if client.getStatus() is False: # Retorna falso se o jogador foi penalizado e tem que ficar parado
        players = {}
        continue

    # jogo esta parado
    if client.isPause() is True: # pergunta se o jogo foi parado no servidor (pelo arquivo main.py)
        time.sleep(5)
        client.setPause()

    # nao recebeu informacoes do pegador
    if client.getTagInfo() is None: # retorna o ID do pegador
        continue

    # verifica se ha posicoes novas
    newposs = client.getPosition() # toda vez que uma posição atualizada (robo informou que esta em uma nova posiçaõ ou a camera detectou que o robo esta em uma nova posição)
    # newposs é uma lista de atualizações recebidas...retorna uma lista vazia se nao tiver novas infos
    for info in newposs:
        posx, posy, course, idd, xsize, ysize, xtag, ytag = info
        if idd != rid: # atualizo as posições de todos os demais robos
            players[idd] = [posx, posy]
    tag, interval = client.getTagInfo()  # retorna o ID do pegador e quando ele começara como pegador, interval é um timestamp

    objectives, dangers = [], [] 
    stoped = False

    if time.time() <= interval: # se pegador ainda nao está "ativo", executo o código abaixo
        # comportamento de fuga
        if tag in players and tag != rid: # o pegador esta na lista de jogadores e eu nao sou pegador
            # foge se nao for pegador 
            dangers.append(players[tag]) # add pegador como um perigo
        else:
            # fica parado
            stoped = True # caso contrario fico parado, pois sou o pegador e aguardo o intervalo para iniciar
    else:

        if len(players) >= 1 and tag == rid: 
            # pega
            for i in players:
                objectives.append(players[i]) # adiciono cada outro jogador como objetivo 

        if tag != rid:
            # foge
            dangers.append(players[tag]) # adiciono o tag como perigo

    
    F, U = potencial(np.array([px, py]), maplines, objectives, dangers) # calculo o campo potencial

    # calcula angulo estre dois vetores
    v = np.array([0, 1]) # referente ao vetor 0,1
    angle = np.math.atan2(np.linalg.det([F,v]),np.dot(F,v))

    F /= 100 # divido a força pq estava forte demais na simulação
    if not stoped:
        px, py = F[0]+px, F[1]+py
        client.setPosition(px, py, angle)
