from rest_framework import serializers
from .models import SubscriptionPlans


class SubscribePlan(serializers.Serializer):
    planName = serializers.CharField(max_length=68)


class WebhookResponse(serializers.Serializer):
    event = serializers.CharField(max_length=256)
