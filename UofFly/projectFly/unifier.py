import scraper
import expedia
import argparse
import datetime

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
			if (flightTime - busTime) > 180:
				pairingCurrent = {
				                    'departure_airport':flight.get('departure_airport'),
									'departure_time':flight.get('departure_time'),
									'price': flight.get('price'),
									'aircraft':flight.get('aircraft'),
									'flight_number': flight.get('flight_number'),
									'airline': flight.get('airline'),
									'arrival_airport': flight.get('arrival_airport'),
									'arrival_time':flight.get('arrival_time'),
									'bus_time': bus
				}
				pairings.append(pairingCurrent)
	for i in pairings:
		print()
		print(i)


