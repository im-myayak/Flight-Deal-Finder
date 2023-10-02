import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('SHEETY_AUTH_TOKEN')
end_point = os.environ.get('SHEETY_END_POINT')


def get_users():
    response = requests.get(url=f"{end_point}/users", headers={"Authorization": api_key})
    response = response.json()['users']
    print(response)
    return response


class User:
    def __init__(self):
        self.firstName = input("Enter the first name: ")
        self.lastName = input("Enter the last name: ")
        self.email = input("Enter the email: ")

    def add_user(self):
        users_from_sheet = get_users()
        emails_from_sheet = [entry["email"] for entry in users_from_sheet]

        if self.email in emails_from_sheet:
            return False
        else:
            while self.email != input("Enter your email again: "):
                self.email = input("Email not matching\n Enter your email: ")
            new = {
                "user": {
                    "firstName": self.firstName,
                    "lastName": self.lastName,
                    "email": self.email,
                }
            }
            response_add = requests.post(url=f"{end_point}/users", json=new,
                                         headers={"Authorization": api_key})
            return response_add

    def update_user(self):
        pass



