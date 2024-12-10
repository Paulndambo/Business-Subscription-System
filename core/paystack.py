from datetime import datetime
import requests
import json
from django.conf import settings
from core.phone_number_validator import validate_phone_number

date_today = datetime.now().date()


class PaystackInterface(object):
    INITIALIZE_PAYMENT_URL = f"{settings.PAYSTACK_BASE_URL}/transaction/initialize"
    PLAN_URL = f"{settings.PAYSTACK_BASE_URL}/plan"
    CUSTOMER_URL = f"{settings.PAYSTACK_BASE_URL}/customer"

    def __init__(self):
        self.headersList = {
            "Accept": "*/*",
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

    def create_customer(self, first_name, last_name, email, phone_number):
        payload = json.dumps(
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone": validate_phone_number(phone_number),
            }
        )

        response = requests.request(
            "POST", url=self.CUSTOMER_URL, data=payload, headers=self.headersList
        )
        res = response.json()["data"]
        return res

    def initialize_payment(self, id, email, amount):
        ref = f"bps_{id}_{date_today.month}_{date_today.year}"

        payload = json.dumps({"email": email, "amount": amount, "reference": ref})

        response = requests.request(
            "POST", self.INITIALIZE_PAYMENT_URL, data=payload, headers=self.headersList
        )
        res = response.json()

        data = res["data"]["authorization_url"]
        return data

    def create_plan(self, name, amount, interval, currency):
        payload = json.dumps(
            {"name": name, "interval": interval, "amount": amount, "currency": currency}
        )

        try:
            response = requests.request(
                "POST", url=self.PLAN_URL, data=payload, headers=self.headersList
            )
            if response.status_code in [201, 200]:
                res = response.json()["data"]
                return res

        except Exception as e:
            print(e)

    def create_subscription(self):
        pass
