#!/usr/bin/env python3
# ____________developed by paco andres_15/04/2019___________________
#from libs import utils
from PYRobot.libs.interfaces import Service


class picam_interface(Service):

    def image(self):
        pass

width=320
height=200
framerate=24
frec=0.2
socket_port =11000
public_sync=False
