from bs4 import BeautifulSoup
# from urllib.request import urlopen
import requests
import json

def find_agents(city, town):
	url = "https://www.wavemoney.com.mm/closest-wave-shop/?lang=&city=" + city + "&town=" + town + "#search-store"

	# url = "https://d3vv6lp55qjaqc.cloudfront.net/items/2W0z3y431R0n0306281t/permalinkhttpswwwwavemoneycomm.txt?X-CloudApp-Visitor-Id=1437757"

	# req = urlopen(url)
	req = requests.get(url)
	data = req.text
	soup = BeautifulSoup(data, "html.parser")
	script = soup.find_all('script')[-1]
	beg = script.string.index("markers = initMarkers(map, ") + 27
	end = beg + script.string[beg:].index(");")
	markers = script.string[beg : end - 4] + "]"

	data = json.loads(markers.replace(":\"", "\":\"").replace("\", ", "\", \"").replace("{ ", "{ \"").replace("),", ")\"").replace(": ", "\": \""))

	for i in data:
		print(i, "\n")

def main():
	find_agents("yangon", "north-okkalapa")


main()