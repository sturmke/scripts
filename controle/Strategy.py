from abc import ABCMeta, abstractmethod
from Movement import *


##
## Dit is een abstracte klasse voor alle mogelijke beweging-strategieen.
##
class AbstractStrategy :
	__metaclass__ = ABCMeta

	## Constructor bij het vehicle dat deze strategie gebruikt.
	def __init__(self, vehicle) :
		self._vehicle = vehicle

	## Geeft aan de beweging-strategie door wat de nieuwe tijd is, zodat die daar gepast
	## op kan reageren door het voertuig te sturen.
	@abstractmethod
	def move(self, time) : pass


## Concrete beweging-strategie waarbij het voertuig niets doet en bijft stilstaan.
class DoNothing (AbstractStrategy) :

	## Constructor
	def __init__(self, vehicle) :
		AbstractStrategy.__init__(self, vehicle)

	## Zet de motoren stil.
	def move(self, time) :
		self._vehicle._wheelRight.setSpeed(0)
		self._vehicle._wheelLeft.setSpeed(0)

##
## Concrete bewegingstrategie waarbij het voertuig blijft doorrijden en in de mate  
## van het mogelijke obstakels tracht te vermijden.
##
class AvoidObstaclesV01 (AbstractStrategy) :

	## Constructor
	def __init__(self, vehicle) :
		AbstractStrategy.__init__(self, vehicle)
		self._direction = ""
		self._turning = False
		#self._startTimeReverseAndTurn = 0
		self._movement = ForwardV01(vehicle)

	## 
	def move(self, time) :
	
		veryClose = 15 # Dichter dan deze afstand van een obstakel zou het voertuig niet mogen komen.
		spotted = 30 # Dit is de afstand waarop we beginnen met reageren op obstakels.
		nothing = 130 # Dit is de afstand waarvan we veronderstellen dat er geen obstakel is.

		
		distanceFront = self._vehicle._sensorFront.getDistance()
		distanceLeft = self._vehicle._sensorLeft.getDistance()
		distanceRight = self._vehicle._sensorRight.getDistance()
		
 		#print distanceLeft, "\t", distanceFront, "\t", distanceRight
		#print "\t\t\t\t", self._vehicle._wheelLeft._speed, "(", self._vehicle._motorLeft._speed, ")", "\t", self._vehicle._wheelRight._speed, "(", self._vehicle._motorRight._speed, ")"

		#self._movement.proceed(time)
		#return
		
		if not self._turning :
		
			if distanceFront >= spotted :

				self._movement.negateNegativeSpeeds()
				self._movement.proceed(time)
			
			elif distanceFront >= veryClose :
				# kijk of er links iets is
				if distanceLeft < spotted :
					self._movement.right(time, 5)
					self._direction = "right"
			
				# kijk of er rechts iets is
				elif distanceRight < spotted :
					self._movement.left(time, 5)
					self._direction = "left"
				else :
					self._movement.proceed(time)
					self._direction = "right"
		
			else :  # distanceFront < veryClose 
			
				if (distanceLeft > veryClose) and (distanceRight > veryClose) :

					if self._direction == "right" :
						self._movement.right(time, 10)   # evt fastRight
					elif self._direction == "left" :
						self._movement.left(time, 10)    # evt fastLeft

				elif (distanceLeft < veryClose) and (distanceRight > veryClose) :
			
					self._movement.right(time, 20)   # evt fastRight
			
				elif (distanceLeft > veryClose) and (distanceRight < veryClose) :
			
					self._movement.left(time, 20)    # evt fastLeft

				elif (distanceLeft < veryClose) and (distanceRight < veryClose) :

					self._turning = True
					self._movement = ReverseAndTurn(self._vehicle)
					self._movement.start(time)
			
		else : # self._turning == True
		
			self._movement.proceed(time)
			if self._movement.finished(time) :
				self._turning = False
				speedsAtEndOfReverseAndTurn = self._movement.getCurrentSpeeds()
				# eventueel gebruiken als beginsnelheden voor de volgende movement
				self._movement = ForwardV01(self._vehicle)



##
## Concrete bewegingstrategie waarbij het voertuig blijft doorrijden en in de mate  
## van het mogelijke obstakels tracht te vermijden.
##
class AvoidObstaclesV02 (AbstractStrategy) :

	## Constructor
	def __init__(self, vehicle) :
		AbstractStrategy.__init__(self, vehicle)
		self._direction = ""
		self._turning = False
		#self._startTimeReverseAndTurn = 0
		self._movement = ForwardV02(vehicle)

	## 
	def move(self, time) :
	
		veryClose = 30 # Dichter dan deze afstand van een obstakel zou het voertuig niet mogen komen.
		spotted = 100 # Dit is de afstand waarop we beginnen met reageren op obstakels.
		nothing = 130 # Dit is de afstand waarvan we veronderstellen dat er geen obstakel is.

		
		distanceFront = self._vehicle._sensorFront.getDistance()
		distanceLeft = self._vehicle._sensorLeft.getDistance()
		distanceRight = self._vehicle._sensorRight.getDistance()
		
 		#print distanceLeft, "\t", distanceFront, "\t", distanceRight
		#print "\t\t\t\t", self._vehicle._wheelLeft._speed, "(", self._vehicle._motorLeft._speed, ")", "\t", self._vehicle._wheelRight._speed, "(", self._vehicle._motorRight._speed, ")"

		#self._movement.proceed(time)
		#return
		
		if not self._turning :
		
			if distanceFront >= spotted :
				if distanceFront >= nothing :
					# reageer niet op obstakels en zet de richting waarnaar we gaan afwijken
					# wanneer er een obstakel gezien wordt terug op 0
					self._direction = ""
				self._movement.setCurrentSpeeds(self._vehicle._defaultSpeed, self._vehicle._defaultSpeed)
				# rij vooruit

			else :
			# obstakel binnen bereik
				if distanceLeft > spotted and distanceRight > spotted :
				# geen obstakel links en rechts
					if self._direction == "" :
						self._direction = "right" # hier kan ook een random waarde gekozen worden
				elif distanceLeft < veryClose and distanceRight > spotted :
				# langs de linkerkant is er een obstakel gedetecteerd, langs de 
				# rechterkant niet, dus begin naar rechts af te draaien	
					self._direction = "right"
				
				elif distanceLeft > spotted and distanceRight < veryClose :
				# langs de rechterkant is er een obstakel gedetecteerd, langs de 
				# linkerkant niet, dus begin naar links te draaien	
					self._direction = "left"
				
				if distanceFront < veryClose :
				# er is langs voor een obstakel heel dichtbij
					if distanceLeft < veryClose and distanceRight < veryClose :
					
						self._turning = True
						self._movement = ReverseAndTurn(self._vehicle)
						self._movement.start(time)
				
					else :
					# er is links of rechts nog ruimte
						if self._direction == "right" :
							# draai om as naar rechts
							self._movement.setCurrentSpeeds(self._vehicle._defaultSpeed, -self._vehicle._defaultSpeed)
						
						elif self._direction == "left" :
							# draai om as naar links
							self._movement.setCurrentSpeeds(-self._vehicle._defaultSpeed, self._vehicle._defaultSpeed)
					
				elif distanceFront < spotted :
				# obstakel opgemerkt op langere afstand
			
					newSpeed = (self._vehicle._defaultSpeed * (distanceFront - veryClose))/(spotted - veryClose)
					# draai in functie van de afstand tot het obstakel sneller of trager
					if self._direction == "right" :
						# draai geleidelijk aan meer naar rechts
						self._movement.setCurrentSpeeds(self._vehicle._defaultSpeed, int(newSpeed))
					elif self._direction == "left" :
						# draai geleidelijk aan meer naar links
						self._movement.setCurrentSpeeds(int(newSpeed), self._vehicle._defaultSpeed)
			
			
			self._movement.proceed(time)

		else : # self._turning == True
			
			if self._movement.finished(time) :
				self._turning = False
				self._movement = ForwardV02(self._vehicle)
				
			self._movement.proceed(time)



##
## Concrete bewegingstrategie waarbij het voertuig luistert naar commando's
##
class RemoteControl (AbstractStrategy) :

	## Constructor
	def __init__(self, vehicle) :
		AbstractStrategy.__init__(self, vehicle)
		self._movement = ForwardV02(vehicle)

	## 
	def move(self, time) :
	
		mode = self._vehicle._steeringMode.getMode()
		
		if mode == "left" :
			self._movement.setCurrentSpeeds(150, 255)
			
		elif mode == "right" :
			self._movement.setCurrentSpeeds(255, 150)
		
		elif mode == "forward" :
			self._movement.setCurrentSpeeds(255, 255)
		
		elif mode == "backward" :
			self._movement.setCurrentSpeeds(-250, -250)
		
		elif mode == "stop" :
			self._movement.setCurrentSpeeds(0, 0)
		
		elif mode == "fastleft" :
			self._movement.setCurrentSpeeds(-250, 250)
		
		elif mode == "fastright" :
			self._movement.setCurrentSpeeds(250, -250)
						
		self._movement.proceed(time)