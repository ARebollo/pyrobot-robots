#!/usr/bin/env python3
# ____________developed by paco andres_15/04/2019___________________
#from libs import utils
import time
from PYRobot.libs import control
from io import BytesIO
import struct
import threading
from PYRobot.libs import control
import PYRobot.libs.utils as utils
import cv2
from components.camera.clientsocket import ClientSocket

class usbcam(control.Control):
    """Set a connection socket to the camera."""
    def __init__(self):
        # Stream settings
        self.buffer = BytesIO()
        self.clients = list()
        self.ip = self._etc["ip"]

    def __Run__(self):
        self.camera = cv2.VideoCapture(self.idcam)
        self.camera.set(cv2.CAP_PROP_FPS, self.framerate)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.start_worker(self.worker_read_usb)
        self.start_thread(self.acceptConnections)
        self.start_thread(self.removeClosedConnections)
        print("abriendo")

    def __Close__(self):
        print("cerrando")
        self.worker_run=False

    def worker_read_usb(self):
        """Main worker."""
        while self.worker_run:
            try:
                l, img = self.camera.read()
                convert= cv2.imencode('.jpeg', img)[1].tobytes()
                self.buffer.write(convert)
            except:
                raise

            senders=[c for c in self.clients if c.status=="open"]
            print("senders ",len(senders))
            if len(senders)>0:
                try:
                    streamPosition = self.buffer.tell()
                    for c in senders:
                        try:
                            if c.connection==0:
                                c.connection =c.serverSocket.accept()[0].makefile("wb")
                            c.connection.write(struct.pack('<L', streamPosition))
                            c.connection.flush()
                        except Exception as e:
                            print("error cerrando")
                            c.setClosed()
                    self.buffer.seek(0)
                    readBuffer = self.buffer.read()
                    senders=[c for c in self.clients if c.status=="open"]
                    for c in senders:
                        try:
                            c.connection.write(readBuffer)
                        except Exception as e:
                            print("cerrando error")
                            c.setClosed()
                    self.buffer.seek(0)
                    self.buffer.truncate()
                except Exception as e:
                    raise
                    utils.format_exception(e)

    def image(self):
        """Return IP and PORT to socket connection """
        print("entrando llamada")
        newClient = ClientSocket(self.socket_port)
        self.clients.append(newClient)
        time.sleep(0.3)
        self.L_info("New Client {}:{}".format(self.ip,newClient.port))
        while newClient.status!="open":
            print("estoy esperando")
            time.sleep(1)
        return self.ip, newClient.port

    def acceptConnections(self):
        while self.worker_run:
            incomming=[c for c in self.clients if c.status=="incomming"]
            print("aceptando conexiones " ,len(incomming))
            for c in incomming:
                #c.acceptConnection()
                print("cambiando a open")
                c.acceptConnection()
            time.sleep(1)

    def removeClosedConnections(self, sec=4):
        """Cleaner. Remove clients marked as closed every "sec" seconds."""
        while self.worker_run:
            time.sleep(sec)
            closed=[c for c in self.clients if c.status=="closed"]
            print("clientes ",len(closed))
            for c in closed:
                c.setClosed()
                print("borrando")
