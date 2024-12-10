from datetime import datetime
import requests
import json
from django.conf import settings

date_today = datetime.now().date()


def generate_payment_link(id, email, amount):
    url = f"{settings.PAYSTACK_BASE_URL}/initialize"

    headersList = {
        "Accept": "*/*",
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    ref = f"bps_{id}_{date_today.month}_{date_today.year}"

    payload = json.dumps({"email": email, "amount": amount, "reference": ref})

    response = requests.request("POST", url, data=payload, headers=headersList)
    res = response.json()

    data = res["data"]["authorization_url"]
    return data
