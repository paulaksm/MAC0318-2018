#!/usr/bin/python
import argparse
import tag
import sys
import cv2
import time
import numpy as np
import os
from cmarkers import getCMarkers, transformMatrixPoints
from util import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n',
                        '--nocamera',
                        action='store_false',
                        help='Disable camera, players need to send the position (default=False)')
    args = parser.parse_args()
    camera = args.nocamera

    cam_id = 1      # id da camera
    device = None   # dipositivo da camera
    dpi = 5         # resolucao para tratamento da imagem
 
    # Dimensoes do campo
    board_size = [185, 215]

    # linhas que descrevem obstaculos
    maplines = [
        [40, 40, 40, 80],
        [40, 80, 60, 80],
        [60, 80, 60, 40],
        [60, 40, 40, 40],

        [40+70, 40+30, 40+70, 80+30],
        [40+70, 80+30, 60+70, 80+30],
        [60+70, 80+30, 60+70, 40+30],
        [60+70, 40+30, 40+70, 40+30]
    ]


    # Se necessario, conecta a camera
    if camera:
        device = open_camera(cam_id)
        board_size = [board_size[1], board_size[0]]

    # Size (in pixels) of the transformed image
    transform_size = (int(board_size[0]*dpi), int(board_size[1]*dpi))
 
    # Calcula a prespectiva
    transform = None
    if camera:
        transform = get_transform_matrix(device, board_size, dpi)
        # Descomente a linha abaixo para entrada manual dos pontos
        # transform = transformMatrixPoints([(340, 10), (78, 1066), (1502, 6), (1806, 1045)], board_size, dpi)

    # Inicia o servidor
    server = tag.TagServer(10318, board_size, maplines)

    while True:
        img_orig = None
        if camera:
            # pega uma imagem da camera
            img_orig = get_frame(device)
        else:
            # cria uma imagem preta
            img_orig = np.zeros([transform_size[0], transform_size[1], 3])

        # contadores para mostrar FPS
        start = time.time()
        if img_orig is not None: # if we did get an image
            img = img_orig

            if camera:
                img = cv2.warpPerspective(img_orig, transform, dsize=transform_size)
                e1 = cv2.getTickCount()

                # identfica os marcadores
                markers = getCMarkers(img)

                # informa o servidor sobre os marcadores
                for i in markers:
                    idd, p, head = i
                    server.updatePosition(idd, p[0]/dpi, p[1]/dpi, head)
                    p = (int(p[0]), int(p[1]))
                    cv2.circle(img, p, 30, (0,255,0))
                    cv2.putText(img, str(idd), p, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255))
            else:
                time.sleep(0.1)

            # mostra os obstaculos
            for line in maplines:
                color = (255, 255, 255)
                line = np.array(line)*dpi
                cv2.line(img, (line[0], line[1]), (line[2], line[3]), color)

            # mostra os robos
            for robot in server.robots():
                for line in robot.lines():
                    p1 = (line[0]*dpi).astype(int)
                    p2 = (line[1]*dpi).astype(int)
                    color = (255, 255, 0)
                    if robot == server.tag:
                        color = (0, 0, 255)
                    cv2.line(img, (p1[0], p1[1]), (p2[0], p2[1]), color)

            # Mostra se o jogo esta em execucao ou nao
            if server.paused:
                cv2.putText(img, "PAUSE", (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

            # Calcula FPS
            end = time.time()
            seconds = end - start
            fps  = 1.0 / seconds
            start = time.time()
            cv2.putText(img, str(fps), (0,60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))
            res = img

            cv2.imshow("warped", res)
 
        else: # if we failed to capture (camera disconnected?), then quit
            break
 
        k = cv2.waitKey(1)
        if k == 115: # s
            server.startGame()
        elif k == 112: # p
            server.stopGame()
        elif k == 113: # q
            server.stop()
            break

    if camera:
        cleanup(cam_id)
