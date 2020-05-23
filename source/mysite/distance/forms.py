from django.db import models
from django import forms
from distance.models import Distance

attributes = {
    'class': 'form-control',
}

class LocationForm(forms.Form):
    origin = forms.CharField(widget=forms.TextInput(attrs=attributes))
    destination = forms.CharField(widget=forms.TextInput(attrs=attributes))
