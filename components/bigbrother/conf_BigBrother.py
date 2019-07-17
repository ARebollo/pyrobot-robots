from PYRobot.libs.interfaces import Service


class BB_interface(Service):

    def Register_Comp(self,name,comp):
        pass
    def Unregister_Robot(self,robot):
        pass
    def Register_Robot(self,robot,default,instances):
        pass
    def Register_Node(self,node,uri):
        pass
    def Unregister_Node(self,node):
        pass
    def Get_Node(self,node):
        pass
    def Get_Robots(self):
        pass
    def Get_Robot(self,robot):
        pass
    def Get_Comp(self,component):
        pass
    def Get_Interface_Uri(self,interface):
        pass
    def Components(self,robot):
        pass
    def Services(self,robot):
        pass
    def Control_Service(self,comp):
        pass
    def Topics(self,robot):
        pass
    def Sub_Topics(self,robot):
        pass
    def Events(self,robot):
        pass
    def Broker(self,robot):
        pass

sys=True
port=9090
broadcast_port=9999
public_sync=False
MQTT_port=1883
mode="public"
KEY="user:pass"
frec=0.02
