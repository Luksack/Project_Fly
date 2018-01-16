import json
import requests
import csv

headers = {'Content-Type': 'application/json'}


def get_ticket_price():
    date_from = "2018-01-21"
    date_to = "2018-01-21"
    api_url = "https://api.ryanair.com/farefinder/3/oneWayFares?&arrivalAirportIataCode=STN" \
              "&departureAirportIataCode=SZZ&language=en&limit=16&market=en-gb&offset=0&outboundDepartureDateFrom=%s" \
              "&outboundDepartureDateTo=%s&priceValueTo=" % (date_from, date_to)
    information = requests.get(api_url, headers=headers)

    if information.status_code == 200:
        return json.loads(information.content)

    else:
        return None

price_info = get_ticket_price()

if price_info is not None:
    for key, value in price_info['fares'][0]['outbound'].items():
        print('{0}: {1}'.format(key, value).replace('\u0142', ''), '\n')
        save = open('test.csv', 'a')
        save.write('{0}: {1}{2}'.format(key, value, '\n').replace('\u0142', ''))
        save.close()
       
else:
    print("[!] Request Failed")

