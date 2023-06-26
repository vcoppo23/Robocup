#send opencv camera feed to laptop via ethernet cable sockets 

# import the necessary packages

import socket
import cv2
import pickle
import struct 
import threading

#create socket
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.1',8089))

#capture video
def capture(camera_num):
    cap=cv2.VideoCapture(camera_num)
    while True:
        ret,frame=cap.read()
        # Serialize frame
        data = pickle.dumps(frame)
        # Send message length first
        message_size = struct.pack("L", len(data))
        # Then data
        clientsocket.sendall(message_size + data)

#start threads
'''
t1 = threading.Thread(target=capture, args=(0,))
t1.start()
t2 = threading.Thread(target=capture, args=(1,))
t2.start()
t3 = threading.Thread(target=capture, args=(2,))
t3.start()
'''