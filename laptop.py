#receive opencv camera stream from socket 

# import the necessary packages
import socket
import time
import cv2
import numpy as np
import sys
import pickle
import struct

# create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.1.2', 8089))
serversocket.listen(10)  # become a server socket, maximum 5 connections

# accept connections from outside
(clientsocket, address) = serversocket.accept()

# receive data from client
data = b""
payload_size = struct.calcsize("L")  # L is unsigned long
while True:
    while len(data) < payload_size:
        data += clientsocket.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += clientsocket.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break