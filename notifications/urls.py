from django.urls import path

from notifications.views import custom_view


urlpatterns = [path("", custom_view, name="custom_view")]
