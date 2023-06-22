#send opencv camera feed to laptop via ethernet cable sockets 

# import the necessary packages

import socket
import time
import cv2
import numpy as np
import sys
import pickle
import struct 

#create socket
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.1',8089))

#capture video
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    # Serialize frame
    data = pickle.dumps(frame)
    # Send message length first
    message_size = struct.pack("L", len(data))
    # Then data
    clientsocket.sendall(message_size + data)


