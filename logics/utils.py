from paystackapi.paystack import Paystack
from datetime import datetime, date
from django.conf import settings
import requests
import resend


paystack_secret_key = settings.PAYSTACKSCKEY
resendKey = settings.RESEND_KEY
paystack = Paystack(secret_key=paystack_secret_key)
resend.api_key = "re_2RTqXv6k_EcECn1Cuur6VY6hCvKxyeWcS"


def CreatePlan(interval: str, name: str, amount: int):
    print(name)
    data = {"name": name, "interval": interval, "amount": str(amount)}
    res = paystack.plan.create(**data)
    print(res)
    return res["data"]["plan_code"]


def CheckNextDueDate(code: str):
    data = paystack.subscription.fetch(code)
    print(data)
    if data["data"]["cancelledAt"] != None:
        dueDate = data["data"]["cancelledAt"]
    else:
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
        "is_subscribed": current_date.date() <= provided_date.date(),
    }

    return response


def send_email(
    email: str,
    subject: str,
    html: str,
    # emailId: int | None,
) -> bool:
    params = {
        "from": "info <info@tscore.ng>",
        "to": [email],
        "subject": subject,
        "html": html,
    }
    resend.Emails.send(params)


def get_filename(filename, request):
    return filename.upper()


def send_notification(id, message, content):
    headers = {"Content-type": ""}
    print(content, message)
