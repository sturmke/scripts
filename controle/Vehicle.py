from BrickPi import *
from Strategy import *
import RPi.GPIO as GPIO  

##
## De klasse Vehicle is verantwoordelijk voor de structuur van het voertuig (motoren en 
## sensoren) en voert een specifieke AbstractStrategy uit. (default is dit een DoNothing)
##
class Vehicle :

	## Constructor met defaultSpeed en assemblage van het voertuig (wielen, motoren en sensoren).
	def __init__(self, defaultSpeed = 200) :
		self._motorLeft = Motor(PORT_D)
		self._motorRight = Motor(PORT_A)
		self._wheelLeft = Wheel(self._motorLeft)
		self._wheelRight = Wheel(self._motorRight)
		self._sensorFront = UltrasonicSensor(PORT_1)
		self._sensorLeft = UltrasonicSensor(PORT_2)
		self._sensorRight = UltrasonicSensor(PORT_4)
		GPIO.setmode(GPIO.BOARD)
		self._blinkerLeft = Blinker(13)
		self._blinkerRight = Blinker(12)
		self._defaultSpeed = defaultSpeed
		self._strategy = DoNothing(self)
		BrickPiSetupSensors()
		

	## Deze methode wordt vanuit de main thread opgeroepen en geeft aan wat de nieuwe
	## tijd is.
	def move(self, time) :
		# Time is de tijd in milliseconden die verkregen wordt van de main thread
		self._strategy.move(time) # Geeft de move door naar de huidig geselecteerde strategy
		
		if self._wheelLeft._speed > self._wheelRight._speed :
			self._blinkerLeft.off()
			self._blinkerRight.on()
			
		elif self._wheelLeft._speed < self._wheelRight._speed :
			self._blinkerLeft.on()
			self._blinkerRight.off()
		
		else :
			self._blinkerLeft.off()
			self._blinkerRight.off()
		
		self._blinkerLeft.move(time)
		self._blinkerRight.move(time)
	
	## Simple-factory methode om een nieuw bewegingsstrategie-object te koppelen
	## aan het voertuig.	
	def setStrategy(self, strategy) :
	
		self._wheelLeft.setSpeed(0)
		self._wheelRight.setSpeed(0)
		if strategy == "DoNothing" :
			self._strategy = DoNothing(self)
		elif strategy == "AvoidObstaclesV01" :
			self._strategy = AvoidObstaclesV01(self)
		elif strategy == "AvoidObstaclesV02" :
			self._strategy = AvoidObstaclesV02(self)
		elif strategy == "RemoteControl" :
			self._strategy = RemoteControl(self)
		else :
			print "Ongeldige Strategy"
			self._strategy = DoNothing(self)

	def setSteeringMode(self, steeringMode) :
		self._steeringMode = steeringMode

## De klasse Blinker 	
class Blinker :

	## Constructor met de GPIO pin waarom de led is aangesloten
	def __init__(self, pin):
		self._pin = pin
		self._state = "off"
		GPIO.setup(self._pin, GPIO.OUT)  

	## Methode om de blinker aan te zetten
	def on(self) :
		self._state = "on"

	## Methode om de blinker af te zetten
	def off(self) :
		self._state = "off"
		
	## Methode die afwisselend een hoog en laag signaal stuurt als de blinker aan is
	def move(self, time) :
		if self._state == "on" :
			if (time % 1000) < 500 :
				GPIO.output(self._pin,GPIO.HIGH) 
			else :
				GPIO.output(self._pin,GPIO.LOW) 
		else :
			GPIO.output(self._pin,GPIO.LOW) 

## De klasse Motor bevat de structuur die nodig is om een motor te beheren.	
class Motor :

	## Constructor met een port die de poort identificeert waarop de motor is 
	## aangesloten.
	def __init__(self, port):
		self._port = port
		self._speed = 0
		BrickPi.MotorEnable[port] = 1

	## Methode om de snelheid van de motor in te stellen.
	def setSpeed(self, speed) :
		self._speed = speed
		BrickPi.MotorSpeed[self._port] = self._speed

## De klasse Wheel bevat de structuur die nodig is om een wiel te beheren.	
class Wheel :

	## Constructor met de motor die het wiel bestuurt
	## een correctie factor kan worden opgegeven om de snelheid
	## van de motor te corrigeren
	def __init__(self, motor, correctie = 1.0):
		self._motor = motor
		self._correctie = correctie
		self._speed = 0

	## Methode om de snelheid van het wiel in te stellen.
	def setSpeed(self, speed) :
		self._speed = speed
		self._motor.setSpeed(int(speed * self._correctie))

## De klasse UltrasonicSensor bevat de structuur die nodig is om een ultrasonic
## sensor te beheren.
class UltrasonicSensor :

	## Constructor met een port die de poort identificeert waarop de sensor is
	## aangesloten.
	def __init__(self, port) :
		self._port = port
		BrickPi.SensorType[port] = TYPE_SENSOR_ULTRASONIC_CONT
	
	## Methode om de waarde die de sensor leest, op te vragen.
	def getDistance(self) :
		return BrickPi.Sensor[self._port]

##
## dit is de klasse die alle mogelijke commando's voor de besturing van
## het voertuig voorstelt
##
class SteeringMode :

	## Constructor 
	def __init__(self) :
		self._mode = "stop"

	def setMode(self, mode) :
	
		if mode == "left" :
			self._mode = mode
		elif mode == "right" :
			self._mode = mode
		elif mode == "forward" :
			self._mode = mode
		elif mode == "backward" :
			self._mode = mode
		elif mode == "stop" :
			self._mode = mode
		elif mode == "fastleft" :
			self._mode = mode
		elif mode == "fastright" :
			self._mode = mode
		else :
			self._mode = "stop"

	def getMode(self) :
		return self._mode
