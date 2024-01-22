from django.urls import path
from .views import CreateSubscription, WebHookListener, TestDataUserRes

urlpatterns = [
    path("subscribe/", view=CreateSubscription.as_view(), name="Create Subscription"),
    path("", TestDataUserRes, name="Testing"),
    path(
        "webhook-listener/", view=WebHookListener.as_view(), name="Transaction Listener"
    ),
]
