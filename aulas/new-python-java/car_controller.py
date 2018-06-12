'''
This code requires keyboard package that can be install with 'pip3 install keyboard'
Must be executed as root
'''
import time
import keyboard as key
import USBInterface

raise_exception = False
try:
    # returns the first brick found and tries to establish connection
    brick = next(USBInterface.find_bricks(debug=False))
    brick.connect()
except usb.core.NoBackendError:
    raise_exception = True
assert raise_exception==0, "No NXT found..."

while True:
    time.sleep(0.05)
    try:
        if key.is_pressed('q'):
            brick.send(99)
            print('Exiting...')
            break
        elif key.is_pressed('up'):
            brick.send(0)
        elif key.is_pressed('right'):
            brick.send(1)
        elif key.is_pressed('left'):
            brick.send(2)
        elif key.is_pressed('down'):
            brick.send(3)
        elif key.is_pressed('space'):
            brick.send(4)
            sonar = brick.recv('i')
            print("\nSonar value: ", sonar)
        elif key.is_pressed('g'):
            brick.send(6)
            msg = brick.recv('s')
            print("\n", msg)
        else:
            brick.send(5)

    except Exception as inst:
        print(inst)
