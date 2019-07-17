
#!/usr/bin/env python3
# ____________developed by paco andres_15/04/2019___________________

from PYRobot.libs.interfaces import Service


class Node_interface(Service):

    def Start_Comp(self,comp):
        pass
    def Stop_Comp(self,comp):
        pass
    def Status_Comp(self,comp):
        pass
    def Kill_Comp(self,comp):
        pass



sys=True
port=5050
public_sync=False
components={}
