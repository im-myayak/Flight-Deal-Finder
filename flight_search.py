from pprint import pprint

from flight_data import FlightData
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import requests

load_dotenv()

auth_token = os.environ.get("TEQUILA_API_KEY")
tequila_END_POINT = "https://tequila-api.kiwi.com/v2/search?"

DEPARTURE_CODE = 'BOM'
today = datetime.now()
DATE_FROM = today + timedelta(days=1)
DATE_TO = today + timedelta(days=30 * 6)


class FlightSearch:
    def __init__(self):
        self.parameters = {
            "fly_from": DEPARTURE_CODE,
            "fly_to": "",
            "date_from": DATE_FROM.strftime("%d/%m/%Y"),
            "date_to": DATE_TO.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "sort": "price",
            "one_for_city": 1,
            "max_stopovers": 2,
            "curr": "USD"
        }

    def get_city_code(self, arrival_city):
        arrival_response = requests.get(
            f'https://tequila-api.kiwi.com/locations/query?term={arrival_city}',
            headers={'apikey': auth_token}
        )
        return arrival_response.json()["locations"][0]['code']

    def searchFlight(self, arrival_city_code):
        self.parameters["fly_to"] = arrival_city_code
        flight_search_response = requests.get(
            url=tequila_END_POINT,
            params=self.parameters,
            headers={'apikey': auth_token}
        )
        response = flight_search_response.json()

        data = response['data'][0]

        if len(data["route"]) == 4:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                arrival_city=data["route"][1]["cityTo"],
                arrival_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][3]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
        elif len(data['route']) == 2:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                arrival_city=data["route"][0]["cityTo"],
                arrival_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )
       
        # print(flight_data.origin_city,
        #       flight_data.origin_airport,
        #       flight_data.arrival_airport,
        #       flight_data.arrival_city,
        #       flight_data.via_city)

        return flight_data
