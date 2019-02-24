import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import argparse

def peoria(date) :
    #date = input("Enter Depart Date in YYYY-MM-DD")
    #print(date)
    website_url = requests.get("https://peoriacharter.com/schedule.php?tt=OW&pickup_location_id=6&drop_off_location_id=47&depart_time=%s&return_time="%date).text
    soup = BeautifulSoup(website_url, 'lxml')
    my_list = soup.find_all('div', {'class':'timesdailyschedule'})

    links = []
    links = my_list
    busses = []
    for link in links:
	    busses.append(link.text)
    return busses


if __name__=="__main__":
	
	argparser = argparse.ArgumentParser()
	argparser.add_argument('date',help = 'MM/DD/YYYY')

	args = argparser.parse_args()
	date = args.date
	
	print ("Fetching bus details")
	scraped_data = peoria(date)

	for i in scraped_data:
		print(i)