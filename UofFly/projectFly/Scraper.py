import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup

def peoria(date) :
    website_url = requests.get("https://peoriacharter.com/schedule.php?tt=OW&pickup_location_id=6&drop_off_location_id=47&depart_time=%s&return_time="%date).text
    soup = BeautifulSoup(website_url, 'lxml')
    my_list = soup.find_all('div', {'class':'timesdailyschedule'})

    links = []
    links = my_list
    busses = []
    for link in links:
	    busses.append(link.text)
    return busses


def callPeoria(date):
	
	print ("Fetching bus details")
	scraped_data = peoria(date)