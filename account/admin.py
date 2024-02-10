from django.contrib import admin
from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from django.urls.resolvers import URLPattern
from .models import User, OneTimePassword
from django.shortcuts import render, get_object_or_404
from notifications.forms import NotificationForm
from notifications.models import Notifications
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import path
from django.contrib.admin import helpers
from logics.utils import send_notification, send_email

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "is_verified",
        "is_subscribed",
        "subscriber_number",
        "get_full_name",
        "date_joined",
        "pk",
    ]
    list_filter = ["is_verified", "is_subscribed"]
    search_fields = ["first_name", "last_name", "email"]
    actions = ["send_not"]

    # change_list_template = "admin/user_details.html"
    def send_not(self, request, queryset):
        notification = get_object_or_404(Notifications, pk=request.POST["notification"])
        emails = [
            send_email(
                user.email, notification.title, f"<html>{notification.content}</html>"
            )
            for user in queryset
        ]
        notification_id = [
            user.notification_id for user in queryset if user.notification_id
        ]

        return HttpResponseRedirect("../user/")

    def changelist_view(self, request, extra_context=None):
        self.change_list_template = "admin/user_details.html"
        extra_context = extra_context or {}
        extra_context["notifications"] = Notifications.objects.all()
        return super().changelist_view(request, extra_context)

    def date_joined(self, obj):
        timestamp_str = str(obj.dateJoined)
        timestamp = datetime.fromisoformat(timestamp_str)
        formatted_date = timestamp.strftime("%d-%B-%y")
        return f"{formatted_date}"


admin.site.register(User, UserAdmin)
admin.site.register(Notifications)
admin.site.register(OneTimePassword)
