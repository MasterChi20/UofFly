import json
import requests

class Leg:
	def __init__(self, mode, org, dest, time, duration, price, flight):
		self.mode = mode
		self.org = org
		self.dest = dest
		self.time = time
		self.duration = duration
		self.price = price
		self.flight = flight
		self.fuel = 0.0

	def getFuel(self):
		URL = "http://www.distance24.org/route.json?stops="
		URL = URL + self.org + "|" + self.dest
		r = requests.get(url = "https://www.distance24.org/route.json?stops=Hamburg|Berlin")
		data = r.json()
		file = open("assets/FlightFuelData.json", "r")
		flightData = json.loads(file.read())
		self.fuel = int(data["distance"])
		if self.mode == "bus":
			return self.fuel
		for x in range(0,len(flightData)):
			if flightData[x]["model"] == self.flight:
				a = float(data["distance"])
				b = float(flightData[x]["fuel"])
				self.fuel = a * b
				break
		return self.fuel


    
class Trip:
	def __init__(self):
		self.legs = []
		self.rank = 0
		self.totalFuel = 0
		self.totalTime = 0

	def addLeg(self, mode, org, dest, time, duration, price, flight):
		currentLeg = Leg(mode, org, dest, time, duration, price, flight)
		currentLeg.getFuel()
		self.totalFuel = self.totalFuel + currentLeg.fuel
		self.legs.append(currentLeg)
