from datetime import datetime
import requests
import json
from django.conf import settings
from core.phone_number_validator import validate_phone_number

date_today = datetime.now().date()


class PaystackInterface(object):
    INITIALIZE_URL = f"{settings.PAYSTACK_BASE_URL}/transaction/initialize"
    PLAN_URL = f"{settings.PAYSTACK_BASE_URL}/plan"
    CUSTOMER_URL = f"{settings.PAYSTACK_BASE_URL}/customer"
    SUBSCRIPTION_URL = f"{settings.PAYSTACK_BASE_URL}/subscription"

    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

    def create_customer(self, first_name, last_name, email, phone_number):
        url = self.CUSTOMER_URL
        payload = json.dumps(
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone": validate_phone_number(phone_number),
            }
        )

        response = requests.request("POST", url=url, data=payload, headers=self.headers)
        res = response.json()["data"]
        return res

    def initialize_payment(self, id, email, amount, plan_code, customer_code):
        ref = f"bps_{id}_{date_today.month}_{date_today.year}"
        url = self.INITIALIZE_URL

        payload = json.dumps({
            "email": email, 
            "amount": amount, 
            "reference": ref,
            "customer": customer_code,
            "plan": plan_code
        })

        response = requests.request("POST", url=url, data=payload, headers=self.headers)
        print(response)
        print(response.text)
        if response.status_code in [201, 200]:
            res = response.json()["data"]
            return res
        else:
            return { "failed": "Something went wrong!" }

    def create_plan(self, name, amount, interval, currency):
        url = self.PLAN_URL
        payload = json.dumps(
            {"name": name, "interval": interval, "amount": amount, "currency": currency}
        )

        try:
            response = requests.request("POST", url=url, data=payload, headers=self.headers)
            if response.status_code in [201, 200]:
                res = response.json()["data"]
                return res

        except Exception as e:
            print(e)

    def create_subscription(self, plan_code, customer_code):
        url = self.SUBSCRIPTION_URL
        payload = json.dumps({
            "customer": customer_code,
            "plan": plan_code
        })

        try:
            response = requests.request("POST", url=url, data=payload, headers=self.headers)
            print(response)
            print(response.text)
            if response.status_code in [201, 200]:
                res = response.json()["data"]
                return res
        except Exception as e:
            print(e)
            raise e
    
