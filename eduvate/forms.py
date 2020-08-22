from django import forms
from django.contrib.auth.forms import UserCreationForm  # Form for signup
from django.contrib.auth.models import User  # Django default user table
from eduvateApp.models import GENDER_STATUS_CHOICES,EDUCATIONAL_STATUS_CHOICES,OCUPATION_STATUS_CHOICES,MARITAL_STATUS_CHOICES,RELIGION_STATUS_CHOICES,SOCIALECONOMIC_STATUS_CHOICES,MENTAL_PROBLEM_CHOICES,TREATMENT_STATUS_CHOICES,KNOWING_WEBSITE_CHOICES


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=10, max_length=15, widget=forms.TextInput(attrs={'class':'form-control form-control-prepended','type':'tel', 'placeholder':'017XXXXXXXX'}))
    password = forms.CharField(required=True, min_length=4, max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control form-control-prepended', 'placeholder':'Enter your password'}))
    full_name = forms.CharField(required=True, min_length=3, max_length=40,widget=forms.TextInput(attrs={'class':'form-control form-control-prepended', 'placeholder':'Your full name'}))
    check = forms.BooleanField(required=True,widget=forms.CheckboxInput(attrs={'class':'custom-control-input', 'type':'checkbox', 'checked':''}))
    age = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'min':1, 'type': 'number', 'placeholder': 'Example: 22'}))
    gender = forms.ChoiceField(required=True, choices=GENDER_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    education = forms.ChoiceField(required=True, choices=EDUCATIONAL_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    marial_status = forms.ChoiceField(required=True, choices=MARITAL_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    ocupation = forms.ChoiceField(required=True, choices=OCUPATION_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    religion = forms.ChoiceField(required=True, choices=RELIGION_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    socio_economic_status = forms.ChoiceField(required=True, choices=SOCIALECONOMIC_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    mental_problem = forms.ChoiceField(required=False,choices=MENTAL_PROBLEM_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    mental_treatment_type = forms.ChoiceField(required=False,choices=TREATMENT_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    knowing_source = forms.ChoiceField(choices=KNOWING_WEBSITE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    medicine_taken_duration = forms.CharField(required=False, max_length=25, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'type': 'tel', 'placeholder': '3 months'}))
    physical_problem = forms.CharField(required=False,max_length=80, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended'}))
    address = forms.CharField(required=True, min_length=3, max_length=80, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'your address'}))


class FeedbackForm(forms.Form):
    quality = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'type':'text', 'data-toggle':'ion-rangeslider', 'data-min':'0', 'data-max':'100', 'data-from':'0', 'data-grid':'true'}))
    satisfaction = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'type':'text', 'data-toggle':'ion-rangeslider', 'data-min':'0', 'data-max':'100', 'data-from':'0', 'data-grid':'true'}))
    good_comment = forms.CharField(max_length=400, required=True,widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended'}))
    bad_comment = forms.CharField(max_length=400,required=True,widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended'}))
    opinion = forms.CharField(max_length=400,required=True,widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended'}))
