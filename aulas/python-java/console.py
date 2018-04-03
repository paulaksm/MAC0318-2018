#!/usr/bin/env python3

import time, usb
import USBInterface

raise_exception = False
try:
    brick = next(USBInterface.find_bricks(debug=False))
    brick.connect()
except usb.core.NoBackendError:
	raise_exception = True
assert raise_exception==0, "No NXT found..."
  
# envia para o robo que esta pronto
brick.send("0")

while True:
    try:
        a = brick.recv()
        print('Tacho count motor A: {}'.format(a))
    except usb.core.USBError as e:
        # Quando a conexao foi encerrada pelo robo
        if e.errno == 32:
           break
brick.close()
