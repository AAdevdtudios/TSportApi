from django import forms


class NotificationForm(forms.Form):
    # _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    title = forms.CharField(
        max_length=100,
    )
    description = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter the notification message here.",
    )
