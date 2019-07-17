#!/usr/bin/env python3
# ____________developed by paco andres____________________
# _________collaboration with cristian vazquez____________
import time
from PYRobot.libs import control
from gevent.server import DatagramServer
from PYRobot.libs.proxy import Proxy



class BigBrother(control.Control):

    def __init__(self):
        self.Comps={}
        self.Robots={}
        self.Nodes={}
        self.host=self._etc["ip"]
        self.port=self._etc["port"]
        self.broadcast=self._etc["broadcast_port"]

    def __Run__(self):
        self.L_info("starting BigBrother")
        self.bcast = DatagramServer(('', self.broadcast), handle=self.receive)
        self.bcast.start()
        self.start_worker(self.cleaner, )


    def __Close__(self):
        self.worker_run=False

    def cleaner(self):
        while self.worker_run:
            delete=[]
            for comp in self.Comps:
                ser=self.Control_Service(comp)
                control=Proxy(ser)
                if not control():
                    delete.append(comp)
            for c in delete:
                del(self.Comps[c])
                self.L_info("{} disconnected".format(c))
            Robots=list(self.Robots)
            for R in Robots:
                if len(self.Components(R))==0:
                    self.Unregister_Robot(R)
                    self.L_info("{} Unregistered ".format(R))
            Nodes=list(self.Nodes)
            delete=[]
            for N in Nodes:
                ser=self.Nodes[N][1][1]
                control=Proxy(ser)
                if not control():
                    delete.append(N)
                for c in delete:
                    del(self.Nodes[N])
                    self.L_info("{} Node disconnected".format(c))
            time.sleep(2)


    def receive(self, data, address):
        if data.decode()=="hi BigBrother":
            send="{}:{}".format(self.host,self.port)
            self.bcast.sendto(send.encode(), address)
        else:
            self.bcast.sendto("0.0.0.0:0".encode(), address)

    def Register_Node(self,node,uri):
        if node not in self.Nodes:
            self.Nodes[node]=uri
            self.L_info("Node {} Registered at {}".format(node,uri))
            return True
        self.L_info("Node {} is on line at {}".format(node,uri))
        return False

    def Unregister_Node(self,node):
        if node in self.Nodes:
            del(self.Nodes[node])
            return True
        return False

    def Get_Node(self,node):
        if node in self.Nodes:
            return self.Nodes[node][0][1]
        else:
            return "0.0.0.0:0"

    def Unregister_Robot(self,robot):
        if robot in self.Robots:
            del(self.Robots[robot])

    def Register_Robot(self,robot,default):
        if robot not in self.Robots:
            self.Robots[robot]={}
            self.Robots[robot]["default"]=default
            self.L_info("Robot {} Registered".format(robot))
            return True
        else:
            return False

    def Get_Robots(self):
        return self.Robots

    def Get_Robot(self,robot):
        default={}
        if robot in self.Robots:
            default=self.Robots[robot]
        return default

    def Register_Comp(self,name,comp):
        general=comp["GENERAL"]
        del(comp["GENERAL"])
        robot=general["robot"]
        if robot not in self.Robots:
            self.Register_Robot(robot,general)
        if name not in self.Comps:
            self.Comps[name]=comp
            self.L_info("Component {} Registered".format(name))
            return True
        else:
            return False

    def Get_Comp(self,name):
        try:
            return self.Comps[name]
        except:
            return {}

    def Components(self,robot):
        return [x for x in self.Comps if x.find(robot+"/")==0]

    def Services(self,robot):
        comps=self.Components(robot)
        ser=[x+"/"+k[0] for x in comps for k in self.Comps[x]["INTERFACES"]
                if k[0]!="Control_Interface"]
        return ser

    def Get_Interface_Uri(self,interface):
        robot,comp,interface=interface.split("/")
        comps=self.Components(robot)
        ser=[k[1] for x in comps for k in self.Comps[x]["INTERFACES"]
                if k[0]==interface]
        if len(ser)==1:
            return ser[0]
        else:
            return "0.0.0.0:0"

    def Control_Service(self,comp):
        if comp in self.Comps:
            interfaces=list(self.Comps[comp]["INTERFACES"])
            ser=[k[1] for k in interfaces if k[0]=="Control_Interface"]
            if len(ser)==1:
                return ser[0]
            else:
                return None

    def Topics(self,robot):
        comps=self.Components(robot)
        top=["{}/{}".format(x,k) for x in comps for k in self.Comps[x]["PUB"]]
        return top

    def Events(self,robot):
        comps=self.Components(robot)
        events=["{}/{}".format(x,k) for x in comps for k in self.Comps[x]["EVENTS"]]
        #events=[k for x in comps for k in self.Comps[x]["EVENTS"]]
        return events

    def Sub_Topics(self,robot):
        comps=self.Components(robot)
        top=[k for x in comps for k in self.Comps[x]["SUB"]]
        return top

    def Broker(self,robot):
        if robot in self.Robots:
            return self.Robots[robot]["default"]["MQTT_uri"]
        else:
            return "0.0.0.0:0"
