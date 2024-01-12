from .models import SubscriptionPlans
from account.serializer import ErrorValidation
from django.conf import settings
import requests


def SubscribeUser(email: str, planName: str):
    paystackSC = settings.PAYSTACKSCKEY
    if SubscriptionPlans.objects.filter(PlanType=planName).exists():
        subscription = SubscriptionPlans.objects.get(PlanType=planName)
        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers={"Authorization": "Bearer " + paystackSC},
            data={
                "email": email,
                "amount": subscription.Price,
                "plan": subscription.PlanCode,
            },
        )
        if response.status_code == 400:
            raise ErrorValidation("Failed to connect", 400)
        data = response.json()
        return data["data"]["authorization_url"]
    raise ErrorValidation("This is serious", 400)


# invoice.create invoice.payment_failed invoice.update subscription.create subscription.disable subscription.not_renew charge.success
def event_type(event, data):
    if event == "invoice.create":
        return
