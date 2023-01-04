# import the necessary packages
from threading import Thread
import cv2
import time
from imutils.video import WebcamVideoStream

class WebcamVideoStream:
	def __init__(self, src=0):
		self.stream = cv2.VideoCapture(src)
		#self.stream = WebcamVideoStream(src=0).start()
		(self.grabbed, self.frame) = self.stream.read()
		self.stopped = False
		self.FPS = 1/30
		self.FPS_MS = int(self.FPS * 1000)

	def start(self):
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		while True:
			if self.stopped:
				return
			'''self.stream.set(cv2.CAP_PROP_FPS, 30)
			self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
			self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
			self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2)
			(self.grabbed, self.frame) = self.stream.read()'''
			time.sleep(self.FPS)

	def read(self):
		return self.frame
		
	def stop(self):
		self.stopped = True    