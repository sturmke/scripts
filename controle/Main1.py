from BrickPi import *
import threading
from Vehicle import *
from Movement import *
from Strategy import *
from abc import ABCMeta, abstractmethod

BrickPiSetup()

##
## Deze klasse beheert de klok en brengt het voertuig hiervan telkens op de hoogte.
##
class myThread (threading.Thread):

	## Constructor met periode die aangeeft om de hoeveel milliseconden
	## het voertuig verwittigd wordt.
	def __init__(self, threadID, name, counter, period = 20.0):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self._period = period
		self._time = 0

	## Run methode die 1 seconde laat verlopen voor de stabilisatie van 
	## sensoren en motoren, en daarna de running-cyclus om elke periode het
	## voertuig te verwittigen via de move-bewerking.
	def run(self):
	
		global vehicle
		vehicle = Vehicle()
		#vehicle.setStrategy("AvoidObstaclesNew")
		vehicle.setStrategy("RemoteControl")
		vehicle.setSteeringMode(steeringMode)
		# negeer 1sec alle sensoren
		while running and (self._time < 1000) : 
			BrickPiUpdateValues()
			time.sleep(self._period / 1000.0)
			self._time = self._time + self._period
		
		while running: 
			vehicle.move(self._time)
			BrickPiUpdateValues()
			time.sleep(self._period / 1000.0)
			self._time = self._time + self._period


print "Press a to toggle the thread"
print "if the thread is running use:"
print "\tao for autonomous control"
print "\trc for remote control"
print "\tz to move forward"
print "\ts to stop"
print "\tq to turn left"
print "\td to turn right"
print "\tr to move in reverse"
running = False
steeringMode = SteeringMode()


while True:
	try:
		
		kb = raw_input("")
		
		if running :
			if kb == "a" :
				running = False
				
			elif kb == "q" :
				steeringMode.setMode("left")
			elif kb == "d" :
				steeringMode.setMode("right")
			elif kb == "z" :
				steeringMode.setMode("forward")
			elif kb == "r" :
				steeringMode.setMode("backward")
			elif kb == "s" :
				steeringMode.setMode("stop")
			elif kb == "ao" :
				vehicle.setStrategy("AvoidObstaclesV02")
			elif kb == "rc" :
				vehicle.setStrategy("RemoteControl")
				
		else :
			if kb == "a" :
				running = True
				thread1 = myThread(1, "Thread1", 1)
				thread1.setDaemon(True)
				thread1.start()
			else :
				running = False
		
		time.sleep(.2)

	except KeyboardInterrupt: # Triggered by pressing Ctrl+C
		running = False # Stop thread
		print "Bye/n"
		break #Exit
