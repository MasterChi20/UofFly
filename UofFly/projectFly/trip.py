import json

class Leg:
	def __init__(self, mode, org, dest, time, duration, price, flight):
		self.mode = mode
		self.org = org
		self.dest = dest
		self.time = time
		self.duration = duration
		self.price = price
		self.flight = flight
		self.fuel = 0
    
class Trip:
	def __init__(self):
		self.legs = []

	def addLeg(self, mode, org, dest, time, duration, price, flight):
		currentLeg = Leg(mode, org, dest, time, duration, price, flight)
		self.legs.append(currentLeg)

	def createFuel(self):
		file = open("assets/fuelEfficiency.json", "r")
		fileJson = json.loads(file.read())
		print(fileJson[0]["fuelBurn"])

if __name__ == '__main__':
	trip = Trip()
	trip.addLeg(trip, "flight", "ord", "blr", 20, 1000, "A330")
	trip.createFuel()