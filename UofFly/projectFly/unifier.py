from . import expedia
from . import scraper
import datetime
import requests
import json

def timeScorer(s):
	if "pm" in s:
		if len(s) == 7:
			hours = int(s[0:2])
			minutes = int(s[3:5])
		else :
			hours = int(s[0:1])
			minutes = int(s[2:4])
		score = hours * 60 + minutes + 720
	else :
		if len(s) == 7:
			hours = int(s[0:2])
			minutes = int(s[3:5])
		else :
			hours = int(s[0:1])
			minutes = int(s[2:4])
		score = hours * 60 + minutes

	return score

def getTime(s):
	return s.get('flight_hour') * 60

def getDistance(org, dest):
		URL = "https://www.distance24.org/route.json?stops="
		URL = URL + org + "|" + dest
		r = requests.get(url = URL)
		data = r.json()
		return data["distance"]
		

def mergeSort(arr): 
    if len(arr) >1: 
        mid = len(arr)//2 #Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSort(L) # Sorting the first half 
        mergeSort(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if L[i]["rank"] < R[j]["rank"]: 
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1

def runner(source, destination, date, weight_time, weight_price):



	formatDate = datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
	scraper.callPeoria(formatDate)
	busses = []
	busses = scraper.peoria(formatDate)
	flights = expedia.parse(source,destination,date)
	pairings = []

	fuel = getDistance(source, destination)

	for bus in busses:
		busTime = timeScorer(bus)
		for flight in flights:
			flightTime = timeScorer(flight.get('departure_time'))
			if (flightTime - busTime) > 420 and (flightTime - busTime) < 600:
				pairingCurrent = {
                    'departure_airport':flight.get('departure_airport'),
					'departure_time':flight.get('departure_time'),
					'price': flight.get('price'),
					'aircraft':flight.get('aircraft'),
					'flight_number': flight.get('flight_number'),
					'airline': flight.get('airline'),
					'arrival_airport': flight.get('arrival_airport'),
					'arrival_time':flight.get('arrival_time'),
					'bus_time': bus,
					'flight_hour': flight.get('flight_hour'),
					'flight_minute': flight.get('flight_minute'),
					'rank': 0.0,
					'fuel': 0.0
				}

				file = open("projectFly/assets/FlightFuelData.json", "r")
				flightData = json.loads(file.read())
				pairingCurrent["fuel"] = float(fuel) / 100.0
				for x in range(0,len(flightData)):
					if flightData[x]["model"] == pairingCurrent["aircraft"]:
						pairingCurrent["fuel"] = float(fuel) * float(flightData[x]["fuel"]) / 100.0
						break
				pairings.append(pairingCurrent)
				


	sum_price = 0
	sum_time = 0


	sorted = []

	for x in range(0,len(pairings)):

		sum_time = sum_time + float(pairings[x]["flight_hour"])
		sum_price = sum_price + float(pairings[x]["price"])

	average_time = float(sum_time)/float(len(pairings))
	average_price = float(sum_price)/float(len(pairings))

	for x in range(0,len(pairings)):
		pairings[x]["rank"] = ((float(pairings[x]["flight_hour"])) * weight_time / average_time) 
		+ ((float(pairings[x]["price"])) * weight_price / average_price) 

	mergeSort(pairings)

	for x in range(0,len(pairings)):
		print(pairings[x]["rank"])
	return pairings