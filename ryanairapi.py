import json
import requests
import csv
import time
import os.path

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
    departure_airport = flight_info['fares'][0]['outbound']['departureAirport']['name']
    departure_code = flight_info['fares'][0]['outbound']['departureAirport']['iataCode']
    arrival_airport = flight_info['fares'][0]['outbound']['arrivalAirport']['name']
    arrival_code = flight_info['fares'][0]['outbound']['arrivalAirport']['iataCode']
    departure_date = flight_info['fares'][0]['outbound']['departureDate']
    arrival_date = flight_info['fares'][0]['outbound']['arrivalDate']
    price = flight_info['fares'][0]['outbound']['price']['value']
    price_currency = flight_info['fares'][0]['outbound']['price']['currencyCode']

    if not os.path.isfile('test.csv'):
        print("Generating file...Please wait...")
        with open('test.csv', 'a') as file:
            my_fields = ['Execution Time', 'Departure Airport', 'Departure Code', 'Arrival Airport', 'Arrival Code',
                         'Departure Date','Arrival Date', 'Price', 'Currency']
            writer = csv.DictWriter(file, fieldnames=my_fields)
            writer.writeheader()
            writer.writerow({'Execution Time': scrap_time,
                             'Departure Airport': departure_airport,
                             'Departure Code': departure_code,
                             'Arrival Airport': arrival_airport,
                             'Arrival Code': arrival_code,
                             'Departure Date': departure_date,
                             'Arrival Date': arrival_date,
                             'Price': price,
                             'Currency': price_currency,
                             })
            print("File Generated")
    else:
        with open('test.csv', 'a') as file:
            data = [scrap_time,
                    departure_airport,
                    departure_code,
                    arrival_airport,
                    arrival_code,
                    departure_date,
                    arrival_date,
                    price,
                    price_currency
                    ]
            writer = csv.writer(file)
            writer.writerow(data)
            print("Information added successfully")


else:
    print("[!] Request Failed")
