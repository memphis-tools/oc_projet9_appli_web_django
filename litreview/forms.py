from django import forms
from django.conf import settings
from litreview import models


class UserFollowForm(forms.Form):
    follow_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    username = settings.AUTH_USER_MODEL


class UnsubscribeForm(forms.Form):
    unsubscribe_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    username = settings.AUTH_USER_MODEL


class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class ReviewCreationForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
