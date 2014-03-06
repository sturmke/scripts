# TROUBLESHOOTING:
#	Don't use Ctrl+Z to stop the program, use Ctrl+c.
#	If you use Ctrl+Z, it will not close the socket and you won't be able to run the program the next time.
#	If you get the following error:
#		"socket.error: [Errno 98] Address already in use "
#	Run this on the terminal:
#		"sudo netstat -ap |grep :9093"
#	Note down the PID of the process running it
#	And kill that process using:
#		"kill pid"
#	If it does not work use:
#		"kill -9 pid"
#	If the error does not go away, try changin the port number '9093' both in the client and server code

from BrickPi import * # import BrickPi.py file to use BrickPi operations
import threading # import threading
import tornado.ioloop # import tornado for websocket control
import tornado.web
import tornado.websocket
import tornado.template
import RPi.GPIO as GPIO # import GPIO for controlling the leds
from Vehicle import *
from Movement import *
from Strategy import *
from abc import ABCMeta, abstractmethod

c=0
#Initialize TOrnado to use 'GET' and load index.html
class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

#Code for handling the data sent from the webpage
class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print 'connection opened...'
		
	def on_message(self, message): # receives the data from the webpage and is stored in the variable message
		print 'received:', message # prints the received message from the webpage 
		
		if message == "forward": # checks for the received data and assigns different values to c which controls the movement of robot.
			print "Running Forward"
			steeringMode.setMode("forward")
		
		if message == "backward":
			print "Running Reverse"
			steeringMode.setMode("backward")
		
		if message == "left":
			print "Turning Left"
			steeringMode.setMode("left")
		
		if message == "right":
			print "Turning Right"
			steeringMode.setMode("right")
		
		if message == "stop":
			print "Stopped"
			steeringMode.setMode("stop")
		
		if message == "fastleft":
			print "Fast left"
			steeringMode.setMode("fastleft")
		
		if message == "fastright":
			print "Fast right"
			steeringMode.setMode("fastright")
		
		if message == "control":
			print "User Control"
			steeringMode.setMode("stop")
			vehicle.setStrategy("RemoteControl")
		
		if message == "autonomous":
			print "Autonomous Control"
			vehicle.setStrategy("AvoidObstaclesV02")

		print "message processed"
	
	def on_close(self):
		print 'connection closed...'

application = tornado.web.Application([
	(r'/ws', WSHandler),
	(r'/', MainHandler),
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

class myThread (threading.Thread):
	def __init__(self, threadID, name, counter, period = 20.0):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self._period = period
		self._time = 0
		
	def run(self):
		print "Ready"
		global steeringMode
		global vehicle
		vehicle = Vehicle()
		steeringMode = SteeringMode()
		vehicle.setSteeringMode(steeringMode)

		while running and (self._time < 1000):
			BrickPiUpdateValues() # Ask BrickPi to update values for sensors/motors
			time.sleep(self._period / 1000.0)
			self._time = self._time + self._period
		
		while running: 
			vehicle.move(self._time)
			BrickPiUpdateValues()
			time.sleep(self._period / 1000.0)
			self._time = self._time + self._period

if __name__ == "__main__":
	BrickPiSetup() # setup the serial port for communication
	running = True
	thread1 = myThread(1, "Thread-1", 1)
	thread1.setDaemon(True)
	thread1.start()  
	application.listen(9093) #starts the websockets connection
	tornado.ioloop.IOLoop.instance().start()