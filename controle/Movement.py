from abc import ABCMeta, abstractmethod

##
## Dit is een abstracte klasse voor alle mogelijke bewegingen.
##
class AbstractMovement :
	__metaclass__ = ABCMeta

	## Constructor waarbij het voertuig dat de beweging moet uitvoeren, wordt doorgegeven.
	def __init__(self, vehicle) :
		self._vehicle = vehicle
		self._targetSpeedLeft = vehicle._defaultSpeed
		self._targetSpeedRight = vehicle._defaultSpeed
		self._currentSpeedLeft = 0
		self._currentSpeedRight = 0
		self._startTime = 0
		self._increment = 0

	## Methode om het begin van de beweging aan te geven.
	def start(self, time) :
		self._startTime = time

	## Geeft aan wat de nieuwe tijd is, zodat de beweging hier gepast op kan reageren
	## om het voertuig te sturen.
	@abstractmethod
	def proceed(self, time) : pass

	## Een test om na te gaan of de beweging ten einde is.
	## De default implementatie is gemaakt voor bewegingen die geen expliciet einde hebben.
	## Concrete bewegingen kunnen deze overschrijven.
	def finished(self, time) :
		return False

	## Methode om de twee targetSpeeds te zetten.
	def setTargetSpeeds(self, left, right) : 
		self._targetSpeedLeft = left
		self._targetSpeedRight = right

	## Methode om de twee targetSpeeds op te vragen.
	def getTargetSpeeds(self) : 
		return {'left': self._targetSpeedLeft, 'right': self._targetSpeedRight}

	##	Methode om de twee currentSpeeds te zetten.
	def setCurrentSpeeds(self, left, right) : 
		self._currentSpeedLeft = left
		self._currentSpeedRight = right

	## Methode om de twee currentSpeeds op te vragen.
	def getCurrentSpeeds(self) : 
		return {'left': self._currentSpeedLeft, 'right': self._currentSpeedRight}

	## Als er een negatieve snelheid is, wordt deze op 0 gezet.
	def negateNegativeSpeeds(self) : 
		if self._currentSpeedLeft < 0 :
			 self._currentSpeedLeft = 0 
		if self._currentSpeedRight < 0 :
			 self._currentSpeedRight = 0 

	## Methode om een nieuwe snelheid te berekenen die dichter bij de target speed zit, 
	## vertrekkende vanaf de current speed.
	def _adjustSpeed(self, current, target) :
		newSpeed = 0
		if abs(current - target) < self._increment :
			newSpeed = target
		elif current < target :
			newSpeed = current + self._increment
		else :
			newSpeed = current - self._increment
		return self._limitSpeed(newSpeed)	
	
	## Methode om de snelheid altijd tussen -self._vehicle._defaultSpeed en 
	## self._vehicle._defaultSpeed te houden
	def _limitSpeed(self, speed) :
		if speed > self._vehicle._defaultSpeed :
			return self._vehicle._defaultSpeed
		elif speed < -self._vehicle._defaultSpeed :
			return -self._vehicle._defaultSpeed
		else :
			return speed

	## Methode om de snelheid van beide motoren te zetten.
	def _updateWheelSpeeds(self) :
		self._vehicle._wheelLeft.setSpeed(self._currentSpeedLeft)
		self._vehicle._wheelRight.setSpeed(self._currentSpeedRight)
	

##
## Deze klasse beschrijft een vooruitgaande rechtlijnige beweging.
##
class ForwardV01 (AbstractMovement) :

	## Constructor met een default increment-waarde van 2
	def __init__(self, vehicle) :
		AbstractMovement.__init__(self, vehicle)
		self._increment = 2

	## Zet de rechtlijnige beweging voort
	def proceed(self, time) :
		self._currentSpeedLeft = self._adjustSpeed(self._currentSpeedLeft, self._targetSpeedLeft)
		self._currentSpeedRight = self._adjustSpeed(self._currentSpeedRight, self._targetSpeedRight)
		self._updateWheelSpeeds()
		
	## Vermindert telkens de linkersnelheid met de increment-waarde maal de factor.
	def left(self, time, factor = 1) :	
		self._currentSpeedLeft = self._limitSpeed(self._currentSpeedLeft - (self._increment * factor))
		self._currentSpeedRight = self._adjustSpeed(self._currentSpeedRight, self._targetSpeedRight)
		self._updateWheelSpeeds()
	
	## Vermindert telkens de rechtersnelheid met de increment-waarde maal de factor.
	def right(self, time, factor = 1) :
		self._currentSpeedLeft = self._adjustSpeed(self._currentSpeedLeft, self._targetSpeedLeft)
		self._currentSpeedRight = self._limitSpeed(self._currentSpeedRight - (self._increment * factor))
		self._updateWheelSpeeds()

	## Vermindert telkens de linkersnelheid met de increment-waarde maal de factor.
	## Vermeerdert telkens de rechtersnelheid met de increment-waarde maal de factor.
	def fastLeft(self, time, factor = 1) :	
		self._currentSpeedLeft = self._limitSpeed(self._currentSpeedLeft - (self._increment * factor))
		self._currentSpeedRight =  self._limitSpeed(self._currentSpeedRight + (self._increment * factor))
		self._updateWheelSpeeds()

	## Vermeerdert telkens de linkersnelheid met de increment-waarde maal de factor.
	## Vermindert telkens de rechtersnelheid met de increment-waarde maal de factor.
	def fastRight(self, time, factor = 1) :
		self._currentSpeedLeft = self._limitSpeed(self._currentSpeedLeft + (self._increment * factor))
		self._currentSpeedRight = self._limitSpeed(self._currentSpeedRight - (self._increment * factor))
		self._updateWheelSpeeds()
	

##
## Deze klasse beschrijft een vooruitgaande rechtlijnige beweging.
##
class ForwardV02 (AbstractMovement) :

	## Constructor 
	def __init__(self, vehicle) :
		AbstractMovement.__init__(self, vehicle)

	## Zet de rechtlijnige beweging voort
	def proceed(self, time) :
		self._updateWheelSpeeds()
		

##
## Deze klasse beschrijft het gedrag waarbij het voertuig achteruit rijdt 
##
class Backward (AbstractMovement) :

	## Constructor met default increment-waarde van 2 en targetSpeeds van -100 en -100.
	def __init__(self, vehicle) :
		AbstractMovement.__init__(self, vehicle)
		self.setTargetSpeeds(-255, -255)
		self._increment = 5

	## Zet de beweging verder.
	def proceed(self, time) :
		self._currentSpeedLeft = self._adjustSpeed(self._currentSpeedLeft, self._targetSpeedLeft)
		self._currentSpeedRight = self._adjustSpeed(self._currentSpeedRight, self._targetSpeedRight)
		self._updateWheelSpeeds()


##
## Deze klasse beschrijft het gedrag waarbij het voertuig in uurwijzerzin rond zijn as omdraait
##
class Turn (AbstractMovement) :

	## Constructor met default increment-waarde van 5 en targetSpeeds van 100 en -100.
	def __init__(self, vehicle) :
		AbstractMovement.__init__(self, vehicle)
		self.setTargetSpeeds(200, -200)
		self._increment = 5

	## Zet het om zijn as draaien verder.
	def proceed(self, time) :
		self._currentSpeedLeft = self._adjustSpeed(self._currentSpeedLeft, self._targetSpeedLeft)
		self._currentSpeedRight = self._adjustSpeed(self._currentSpeedRight, self._targetSpeedRight)
		self._updateWheelSpeeds()


##
## Deze klasse beschrijft het gedrag waarbij het voertuig eerst even achteruit rijdt
## en dan 180 graden rond zijn as omdraait
##
class ReverseAndTurn (AbstractMovement) :

	## Constructor waarin al de twee bewegingsobjecten worden aangemaakt waaruit
	## deze beweging bestaat.
	def __init__(self, vehicle) :
		AbstractMovement.__init__(self, vehicle)
		self._backward = Backward(vehicle)
		self._turn = Turn(vehicle)
		self._startTimeReverseAndTurn = 0
		self._finished = False
		
	## Deze methode onthoudt het starttijdstip van deze beweging en zet de huidige snelheden
	## van de twee gebruikte bewegingen allebei op 0.
	def start(self, time) :	
		self._startTimeReverseAndTurn = time
		self._backward.setCurrentSpeeds(0, 0)
		self._turn.setCurrentSpeeds(0, 0)

	## Zet de beweging verder.
	## Op basis van de verlopen tijd wordt deze proceed eerst doorgestuurd naar de Backward beweging
	## en hierna naar de Turn beweging. Bepaalt ook wanneer deze beweging gedaan is.
	def proceed(self, time) :
		timeReverse = 1500 # tijd in milliseconden dat er achteruitgereden wordt
		timeTurn = 2000 # tijd in milliseconden dat er gedraaid wordt (+- 180 graden)
		timeReverseAndTurn = time - self._startTimeReverseAndTurn
				
		if timeReverseAndTurn < timeReverse :
			self._backward.proceed(time)
			
		elif timeReverseAndTurn  < (timeReverse + timeTurn) :
			self._turn.proceed(time)
		
		else :
			self._finished = True

	## Geeft aan of deze beweging klaar is met uitvoeren.
	def finished(self, time) :
		return self._finished