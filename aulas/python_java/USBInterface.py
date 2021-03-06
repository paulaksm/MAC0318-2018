# USB socket communication with LEGO Mindstorms NXT -- adapted from nxt-python library
# Copyright (C) 2006, 2007  Douglas P Lau
# Copyright (C) 2009  Marcus Wanner
# Copyright (C) 2011  Paul Hollensen, Marcus Wanner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import usb, os

ID_VENDOR_LEGO = 0x0694
ID_PRODUCT_NXT = 0x0002

IN_ENDPOINT  = 0x82
OUT_ENDPOINT = 0x01

NXT_CONFIGURATION = 1
NXT_INTERFACE     = 0

class USBInterface(object):
    'Object for USB connection to NXT'

    bsize = 60  # USB socket block size

    type = 'usb'

    def __init__(self, device, debug=False):
        self.device = device
        self.debug = debug

    def __str__(self):
        return "USB {}".format(self.device)

    def connect(self):
        #'Use to connect to NXT.'
        if self.debug:
            print ('Connecting via USB...')
        try:
            if self.device.is_kernel_driver_active(NXT_INTERFACE):
                self.device.detach_kernel_driver(NXT_INTERFACE)
            self.device.set_configuration(NXT_CONFIGURATION)
        except Exception as err:
            if self.debug:
                print ('ERROR:usbsock:connect', err)
            raise
        if self.debug:
            print ('Connected.')

    def close(self):
        #'Use to close the connection.'
        if self.debug:
            print ('Closing USB connection...')
        self.device = None
        if self.debug:
            print ('USB connection closed.')

    def send(self, data):
        #'Use to send raw data over USB connection ***ADVANCED USERS ONLY***'
        if self.debug:
            print ('Send:',end=" ")
            print (': {}'.format(ord(data)))
        # O conteudo de data eh enviado do mestre para o escravo
        self.device.write(OUT_ENDPOINT, data, NXT_INTERFACE) 

    def recv(self):
        #'Use to recieve raw data over USB connection ***ADVANCED USERS ONLY***'
        # data recebe dados de um device nxt conectado
        data = self.device.read(IN_ENDPOINT, 64, 1000)
        if self.debug:
            print ('Recv:', end=" ")
            print (':'.join('{}'.format(c & 0xFF) for c in data))
        return ''.join(chr(d & 0xFF) for d in data)

def find_bricks(host=None, name=None, debug=False):
    #'Use to look for NXTs connected by USB only. ***ADVANCED USERS ONLY***'
    for device in usb.core.find(find_all=True, idVendor=ID_VENDOR_LEGO, idProduct=ID_PRODUCT_NXT):
        yield USBInterface(device, debug)


