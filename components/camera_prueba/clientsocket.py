#!/usr/bin/env python3
# ____________developed by paco andres_15/04/2019___________________
#from libs import utils
import time
from io import BytesIO
import socket
import struct
import threading

class ClientSocket(object):
    """Class for Clients of Camera"""

    def __init__(self, port=9000, ):
        self.port = port
        self.serverSocket = socket.socket()
        self.connection =0
        self.status="incomming"
        self.newPort()

    def newPort(self):
        """Check if a port is available, and if it is, assign it, otherwise continue testing the next one."""
        result = 0
        while result is 0:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', self.port))
                if result is 0:
                    self.port += 1
                else:
                    self.serverSocket.bind(('0.0.0.0', self.port))
                    self.serverSocket.listen(0)
                    self.status="incomming"
            except Exception as e:
                print(e)
                utils.format_exception(e)
                self.status="closed"

    def acceptConnection(self):
        """ Accept connections from servers to clients"""
        #self.connection =self.serverSocket.accept()[0].makefile("wb")
        time.sleep(0.2)
        self.status="open"


    def getClient(self):
        """ Return client information"""
        return self.port, self.serverSocket, self.connection

    def setClosed(self):
        """ Set client as closed """
        print("CAM-Client disconnected: {}".format(self.port))
        try:
            self.connection.write(struct.pack('<L', 0))
            self.connection.close()
            self.serverSocket.close()
            self.status="closed"
        except Exception:
            raise
        if exception is not None:
            utils.format_exception(exception)
