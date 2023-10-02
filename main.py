import requests
import os
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from users import User
from dotenv import load_dotenv

load_dotenv()
auth_token = os.environ.get("TEQUILA_API_KEY")
api_key = os.environ.get('SHEETY_AUTH_TOKEN')

end_point = os.environ.get('SHEETY_END_POINT')

# print("Welcom to Yaya's Flight Club.\nWe find the best flight deals and email you")
# user_object = User()
# response = user_object.add_user()
# if not response:
#     print("Emails already exists")
#     response = user_object.add_user()
# print("You have done!")
dataManager = DataManager()
flightSearcher = FlightSearch()
sheet_data = dataManager.get_google_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row['iataCode'] = flightSearcher.get_city_code(row['city'])
    dataManager.googleSheet_Data = sheet_data
    dataManager.update_google_data()
for city in sheet_data:
    flight_data = flightSearcher.searchFlight(city["iataCode"])

    if flight_data and flight_data.price <= city['lowestPrice']:
        notificationManager = NotificationManager()
        message = f"Low price alert! Only USD {flight_data.price} to fly from {flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.arrival_city}-{flight_data.arrival_airport}, from {flight_data.out_date} to {flight_data.return_date}"
        message_to_send = message if flight_data.stop_overs <= 0 else f"{message}\nFlight has {flight_data.stop_overs} stop, via {flight_data.via_city} City"
        response = notificationManager.send_sms(message_to_send)
        print("SMS: ", response)
        response = notificationManager.send_emails(message=message_to_send, receiver_email="mykourouma32@gmail.com")
        print("EMAIL: ", response)

