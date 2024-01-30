from django.contrib import admin
from .models import User, OneTimePassword
from django.shortcuts import render
from notifications.forms import NotificationForm
from notifications.models import Notifications
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# Register your models here.


class NotificationInline(admin.TabularInline):
    model = Notifications
    extra = 1


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
    inlines = [NotificationInline]

    actions = ["send_notifications", "redirect_users"]

    def redirect_users(self, request, queryset):
        selected = queryset.values_list("id", flat=True)
        selected_ids = ",".join(str(id) for id in selected)
        custom_url = reverse("custom_view") + "?ids=" + selected_ids
        return HttpResponseRedirect(custom_url)

    def date_joined(self, obj):
        timestamp_str = str(obj.dateJoined)
        timestamp = datetime.fromisoformat(timestamp_str)
        formatted_date = timestamp.strftime("%d-%B-%y")
        return f"{formatted_date}"

    def send_notifications(self, request, queryset):
        if "apply" in request.POST:
            title = request.POST["title"]
            description = request.POST["description"]
            print(title)
            print(description)
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = NotificationForm()
        return render(
            request, "admin/send_notification.html", {"users": queryset, "form": form}
        )


admin.site.register(User, UserAdmin)
admin.site.register(Notifications)
admin.site.register(OneTimePassword)
