from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Driver,Rider
from django.forms.fields import DateInput, DateField, NumberInput

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100,required=True)
    phone = forms.NumberInput()
    cardInfo = forms.NumberInput()
    class Meta:
        model = Rider
        fields = ['username','email','password1','password2','first_name','last_name','phone','cardInfo']

class UserEditInfoForm(forms.Form):
    email = forms.EmailField()
    phone = forms.IntegerField()
    cardInfo = forms.IntegerField()
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100,required=True)
    

class DateInput(forms.DateInput):
    input_type = 'date'

class DriverRegistrationForm(forms.Form):
    DOB = forms.DateField(label='Date of Birth',required=True,
                                input_formats = ['%Y-%m-%d'],
                                widget=DateInput(format='%Y-%m-%d'))
    licenseNum = forms.CharField(label='License No.',required=True)
    Vtype = forms.ChoiceField(label='Vehicle Type',choices=(("Sedan", "Sedan"),("SUV", "SUV")))
    brand = forms.CharField(label='Vehicle Brand',required=True)
    model = forms.CharField(label='Vehicle Model',required=True)
    plateNum = forms.CharField(label='Plate No.',required=True)
    max_pnum = forms.IntegerField(label='Max Passenger No.',required=True)
    special_info = forms.CharField(label='Special Info',required=False)
    
    class Meta:
        model = Driver
        fields = ['DOB','licenseNum','Vtype','brand','model','plateNum','max_pnum','special_info']