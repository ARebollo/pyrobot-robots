#!/usr/bin/env python3
# ____________developed by paco andres____________________
# _________collaboration with cristian vazquez____________
import time
import sys
from PYRobot.libs import control
from PYRobot.libs.proxy import Proxy
from PYRobot.libs.botlogging.coloramadefs import P_Log
import PYRobot.libs.utils as utils

robots_dir=utils.get_PYRobots_dir()
sys.path.append(robots_dir)

class Node(control.Control):

    def __init__(self):
        pass

    def __Run__(self):
        self.BB=self._PROC["BB_proxy"]
        self.node=self._PROC["info"]
        self.name=self._etc["host"]
        if self.BB():
            self.BB.Register_Node(self.name,self.node)
            self.L_info("Node {} Registered at {}".format(self.name,self.node))
        else:
            self.L_error("BigBrother no found")

    def __Close__(self):
        pass

    def Start_Comp(self,comp):
        print("starting",comp)
    def Stop_Comp(self,comp):
        print("stopping comp")
    def Status_Comp(self,comp):
        print("status comp")
    def Kill_Comp(self,comp):
        print("killing comp")
