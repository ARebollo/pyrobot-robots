#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# lock().acquire()
# ____________developed by paco andres____________________
import time
from PYRobot.libs import control
import time
import atexit

from Adafruit_MotorHAT import Adafruit_MotorHAT

class MotorHat(control.Control):

    def __init__(self):
        pass

    def __Run__(self):
        self.start_worker(self.worker_reader, )
        print(self.__dict__)

    def __Close__(self):
        self.worker_run=False

    def worker_reader(self):
        while self.worker_run:
            time.sleep(self._etc["frec"])

    def set_base(self,mi,md):
        pass
    def get_base(self):
        pass
