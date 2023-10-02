import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('SHEETY_AUTH_TOKEN')
end_point = os.environ.get('SHEETY_END_POINT')


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.googleSheet_Data = {}

    def get_google_data(self):
        response = requests.get(url=f"{end_point}/prices", headers={"Authorization": api_key})
        self.googleSheet_Data = response.json()['prices']

        return self.googleSheet_Data

    def update_google_data(self):
        for row in self.googleSheet_Data:
            new_data = {
                "price": {
                    "iataCode": row['iataCode']
                }
            }
            rowID = row['id']
            response_update = requests.put(url=f"{end_point}/{rowID}", json=new_data,
                                           headers={"Authorization": api_key})
        return response_update.text
