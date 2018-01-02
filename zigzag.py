import requests
from bs4 import BeautifulSoup
import json

# a function which finds money agents closest to a user in myanmar
# input: string city and town in myanmar (indexed by wave money)
# output: json-formatted list of dictionaries describing money agents in the area (name, address, phone, gps coordinates, web address)

# note to laurent: this function effectively scrapes the entire country indexed on wave money.
# three external modules are used to fetch web data, scrape data, and parse into json respectively
# if we were to use other providers for data, we could expand our method by writing functions to scrape data (or access apis) from these other sources
# we would need to ensure that all data is homogenous, so when formatting into json we should keep only the intersecting data fields (likely name, phone, address, + gps loc)


def find_agents(city, town):

	# read data from dynamic url using requests module

	url = "https://www.wavemoney.com.mm/closest-wave-shop/?lang=&city=" + city + "&town=" + town + "#search-store"
	req = requests.get(url)
	data = req.text

	# parse html data using BeautifulSoup
	# the last script tag is the one which contains relevant loc data

	soup = BeautifulSoup(data, "html.parser")
	script = soup.find_all('script')[-1]

	# get indices of js var containing useful data
	beg = script.string.index("markers = initMarkers(map, ") + 27
	end = beg + script.string[beg:].index(");")

	# adjust string into a json-parseable format

	markers = script.string[beg : end - 4] + "]"
	replacements = {":\"": "\":\"", "\", ": "\", \"", "{ ": "{ \"", "),": ")\"", ": ": "\": \""}

	for i, j in replacements.items():
		markers = markers.replace(i, j)

	data = json.loads(markers)

	# we now have a json object containing store name, phone, address, gps locations
	# gps loc a bit messy (written as a js object init, can be fixed with simple string splicing)

	for i in range(0, len(data)):
		el = data[i]
		el["latLng"] = el["latLng"][22:]
		data[i] = el

	# return formatted json obj with easily retrievable data

	return data

def main():
	# variable inputs, can enter any city and town as long as the string matches the option values in the html
	# reproduced for your convenience here: https://cl.ly/obrS

	agencies = find_agents("danubyu", "danuphyuayeyarwady")
	
	for agency in agencies:
		print(agency, "\n")


main()