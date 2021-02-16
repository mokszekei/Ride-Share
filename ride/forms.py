from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms.fields import DateTimeField

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class RequestForm(forms.Form):
    destination = forms.CharField(label='Destination', max_length=100, required=True)

    arrival_time = DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        )

    party_size = forms.IntegerField(label='Number of Passengers', required=True,
                              validators=[MinValueValidator(1), MaxValueValidator(6)])
    vehicle = forms.ChoiceField(label='Vehicle Type',
                              choices=(("Sedan", "Sedan"),
                                       ("SUV", "SUV")))

    sharable = forms.BooleanField(required=False)
    special_request = forms.CharField(label='Special Request', max_length=100,required=False)
    # edit_id = forms.IntegerField(widget=forms.HiddenInput(),required=True)

class SharedForm(forms.Form):
    # name = forms.CharField(label='Your Email', max_length=200, required=True)
    dest = forms.CharField(label='Destination', max_length=100, required=True)
    earliest_arrival = DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        )
    latest_arrival = DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        )
    pnum = forms.IntegerField(label='Number of Passengers', required=True, validators=[MinValueValidator(1), MaxValueValidator(6)])