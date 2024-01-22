from paystackapi.paystack import Paystack
from datetime import datetime, date
from django.conf import settings
import requests

paystack_secret_key = settings.PAYSTACKSCKEY
paystack = Paystack(secret_key=paystack_secret_key)


def CreatePlan(interval: str, name: str, amount: int):
    print(name)
    data = {"name": name, "interval": interval, "amount": str(amount)}
    res = requests.post(
        "https://api.paystack.co/plan",
        json=data,
        headers={
            "Authorization": f"Bearer {paystack_secret_key}",
            "content-type": "application/json",
        },
    )
    # res = paystack.plan.create(**data)
    print(res.json())
    return "Data"


def CheckNextDueDate(code: str):
    data = paystack.subscription.fetch(code)
    dueDate = data["data"]["next_payment_date"]
    email_token = data["data"]["email_token"]

    if dueDate is None:
        return False
    current_date = datetime.now()
    print(data)
    print(dueDate)
    provided_date = datetime.fromisoformat(dueDate.replace("Z", "+00:00"))
    response = {
        "email_token": email_token,
        "is_subscribed": current_date.date() == provided_date.date(),
    }

    return response
