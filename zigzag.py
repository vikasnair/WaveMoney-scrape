import requests
import json
from bs4 import BeautifulSoup

# a function which finds money agents closest to a user in myanmar
# @params string city, string town (locations in myanmar indexed by wave money)
# @returns json-formatted list of dictionaries describing agents in the area
# (name, address, phone, gps coordinates, web address)


def find_agents(city, town):

    # read data from dynamic url using requests module

    url = 'https://www.wavemoney.com.mm/closest-wave-shop/'
    params = '?lang=&city=' + city + '&town=' + town + '#search-store'
    req = requests.get(url + params)
    data = req.text

    # parse html data using BeautifulSoup
    # the last script tag is the one which contains relevant loc data

    soup = BeautifulSoup(data, "html.parser")
    script = soup.find_all('script')[-1]

    # get indices of js var containing useful data
    beg = script.string.index("markers = initMarkers(map, ") + 27
    end = beg + script.string[beg:].index(");")

    # adjust string into a json-parseable format

    markers = script.string[beg: end - 4] + "]"
    replacements = {":\"": "\":\"", "\", ": "\", \"", "{ ": "{ \"", "),": ")\"", ": ": "\": \""}

    for i, j in replacements.items():
        markers = markers.replace(i, j)

    data = json.loads(markers)

    # we now have a json object containing store name, phone, address, gps loc
    # gps loc a bit messy, can be fixed with some parsing

    for i in range(0, len(data)):
        el = data[i]
        el["latLng"] = el["latLng"][22:]
        data[i] = el

    # return formatted json obj with easily retrievable data

    return data


def main():
    # variable inputs, can enter any city and town
    # as long as the string matches the option values in the html
    # reproduced for your convenience here: https://cl.ly/obrS

    agencies = find_agents("danubyu", "danuphyuayeyarwady")

    for agency in agencies:
        print(agency, "\n")


if __name__ == '__main__':
    main()
