from urllib.request import urlopen
import json

def find_agents():
	


def main():
	# url = "https://www.wavemoney.com.mm/wp-json/contact-form-7/v1"

	url = "https://d3vv6lp55qjaqc.cloudfront.net/items/2W0z3y431R0n0306281t/permalinkhttpswwwwavemoneycomm.txt?X-CloudApp-Visitor-Id=1437757"
	req = urlopen(url)
	data = json.loads(req.read().decode().replace(":\"", "\":\"").replace("\", ", "\", \"").replace("{ ", "{ \"").replace("),", ")\"").replace(": ", "\": \""))

	

main()