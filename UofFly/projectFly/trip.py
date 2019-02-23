class Leg:
	def __init__(self, mode, org, dest, time, duration, price, flight):
    	self.mode = mode
    	self.org = org
    	self.dest = dest
    	self.time = time
    	self.duration = duration
    	self.price = price
    	self.flight = flight
    
class Trip:
	def __init__(self):
		self.legs = []

	def addLeg(mode, org, dest, time, duration, price, flight):
		currentLeg = Leg(mode, org, dest, time, duration, price, flight)
		self.append(currentLeg)