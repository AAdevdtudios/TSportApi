from django.db import models

SUBSCRIPTIONTYPE = {
    "silver": "silver",
    "gold": "gold",
    "premium": "premium",
    "diamond": "diamond",
}


# Create your models here.
class SubscriptionPlans(models.Model):
    PlanType = models.CharField(max_length=50, default=SUBSCRIPTIONTYPE.get("silver"))
    PlanCode = models.CharField(max_length=256)
    Price = models.IntegerField()
