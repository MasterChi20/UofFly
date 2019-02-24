import scraper
import expedia
import argparse
import datetime
import trip

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

if __name__ == "__main__" :
	argparser = argparse.ArgumentParser()
	argparser.add_argument('source',help = 'Source airport code')
	argparser.add_argument('destination',help = 'Destination airport code')
	argparser.add_argument('date',help = 'MM/DD/YYYY')



	args = argparser.parse_args()
	source = args.source
	destination = args.destination
	date = args.date
	formatDate = datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")

	date = args.date
	busses = []
	busses = scraper.peoria(formatDate)
	flights = expedia.parse(source,destination,date)
	pairings = []

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
					'rank': 0.0
				}
				pairings.append(pairingCurrent)

	min_price = 5000.0
	max_price = 0.0

	min_travel_time = 72.0
	max_travel_time = 0.0

	weight_time = 1.0
	weight_price = 0.0

	sorted = []

	for x in range(0,len(pairings)):
		if float(pairings[x]["flight_hour"]) > max_travel_time:
			max_travel_time = float(pairings[x]["flight_hour"])

		if float(pairings[x]["flight_hour"]) < min_travel_time:
			min_travel_time = float(pairings[x]["flight_hour"])

		if float(pairings[x]["price"]) < min_price:
			min_price = float(pairings[x]["price"])

		if float(pairings[x]["price"]) > max_price:
			max_price = float(pairings[x]["price"])

	dif_price = max_price - min_price
	dif_travel_time = max_travel_time - min_travel_time

	for x in range(0,len(pairings)):
		pairings[x]["rank"] = ((float(pairings[x]["flight_hour"]) - min_travel_time) * weight_time / dif_travel_time) 
		+ ((float(pairings[x]["price"]) - min_price) * weight_price / dif_price) 

	mergeSort(pairings)

	for x in range(0, len(pairings)):
		print(pairings[x]["airline"])
