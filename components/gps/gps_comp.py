#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# lock().acquire()
# ____________developed by paco andres____________________
import time
from PYRobot.libs import control
import json
from PYRobot.libs.proxy import Proxy

class gps(control.Control):

    def __init__(self):
        self.X=0.1
        self.Y=0.2
        self.Z=0.5
        self.frec=0.02

    def __Run__(self):
        print("init gps")
        self.start_worker(self.worker_reader, )
        #self.New_handler("base_event",self.on_base)

    def worker_reader(self):

        while self.worker_run:
            #print("el valor de base ",self.base)
            self.X=round(self.X+0.1,2)
            self.Y=round(self.Y+0.2,2)
            self.Z=round(self.Z+0.4,2)
            #self.L_info(" md:{},mi:{}, baseE:{}".format(self.md,self.mi,self.base_event))
            time.sleep(self.frec)

    def get_localization(self):
        pass

    def set_localization(self,x,y,z):
        self.X=x
        self.Y=y
        self.Z=z


    def on_base(self,channel,msg):
        self.L_info("on {} {}".format(channel,msg))
