'''
This code requires keyboard package that can be install with 'pip3 install keyboard'
Must be executed as root
'''
import time
import keyboard as key
import USBInterface

raise_exception = False
try:
    # retorna o primeiro brick encontrado pelo metodo find_bricks e faz a conexao
    brick = next(USBInterface.find_bricks(debug=False))
    brick.connect()
except usb.core.NoBackendError:
    raise_exception = True
assert raise_exception==0, "No NXT found..."

while True:
    time.sleep(0.05)
    try:
        if key.is_pressed('q'):
            brick.send('\x64')
            print('Exiting...')
            break
        elif key.is_pressed('up'):
            brick.send('\x01')
       else:
            brick.send('\x05')

    except Exception as inst:
        print(inst)
