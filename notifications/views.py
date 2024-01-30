from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import NotificationForm
from .models import Notifications
from django.contrib import admin
from account.models import User


def custom_view(request):
    data = request.GET.get("ids", None)
    if data:
        id_list = [int(id) for id in data.split(",")]
        queryset = User.objects.filter(id__in=id_list)
    else:
        queryset = User.objects.none()

    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            for user in queryset:
                notification = Notifications(
                    user=user, title=title, description=description
                )
                notification.save()
        else:
            print(form.errors)
    else:
        form = NotificationForm()
    return render(
        request, "admin/send_notification.html", {"users": queryset, "form": form}
    )


def send_notification(modeladmin, request, queryset):
    if "apply" in request.POST:
        form = NotificationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            for user in queryset:
                Notifications.objects.create(
                    user=user,
                    message=message,
                )
            modeladmin.message_user(request, "Notification sent to selected users.")
            return HttpResponseRedirect(request.get_full_path())

        return HttpResponseRedirect(request.get_full_path())

    form = NotificationForm(
        initial={"_selected_action": request.POST.getlist(admin.ACTION_CHECKBOX_NAME)}
    )
    return render(
        request,
        "admin/send_notification.html",
        {"users": queryset, "notification_form": form},
    )


send_notification.short_description = "Send notification to selected users"
