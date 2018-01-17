import json
import requests
import csv
import time

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


flight_info = get_ticket_price()

if flight_info is not None:
    scrap_time = time.asctime(time.localtime(time.time()))
    departureAirport = flight_info['fares'][0]['outbound']['departureAirport']['name']
    departureCode = flight_info['fares'][0]['outbound']['departureAirport']['iataCode']
    arrivalAirport = flight_info['fares'][0]['outbound']['arrivalAirport']['name']
    arrivalCode = flight_info['fares'][0]['outbound']['arrivalAirport']['iataCode']
    departureDate = flight_info['fares'][0]['outbound']['departureDate']
    price = flight_info['fares'][0]['outbound']['price']['value']
    price_currency = flight_info['fares'][0]['outbound']['price']['currencyCode']
    csv_information = [["Execution Time","Departure Airport", "Departure Code", "Arrival Airport", "Arrival Code", "Departure Date", "Price",
             "Currency"],
            [scrap_time, departureAirport, departureCode, arrivalAirport, arrivalCode, departureDate, price, price_currency]]

    file = open('test.csv', 'a')
    with file:
        writer = csv.writer(file)
        writer.writerows(csv_information)


else:
    print("[!] Request Failed")
