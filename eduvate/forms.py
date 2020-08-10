from django import forms
from django.contrib.auth.forms import UserCreationForm  # Form for signup
from django.contrib.auth.models import User  # Django default user table
from instructorApp.models import Country


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=10, max_length=15, widget=forms.TextInput(attrs={'class':'form-control form-control-prepended','type':'tel', 'placeholder':'017XXXXXXXX'}))
    password = forms.CharField(required=True, min_length=4, max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control form-control-prepended', 'placeholder':'Enter your password'}))
    full_name = forms.CharField(required=True, min_length=3, max_length=40,widget=forms.TextInput(attrs={'class':'form-control form-control-prepended', 'placeholder':'Your full name'}))
    check = forms.BooleanField(required=True,widget=forms.CheckboxInput(attrs={'class':'custom-control-input', 'type':'checkbox', 'checked':''}))
    age = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'min':1, 'type': 'number', 'placeholder': 'Example: 22'}))
    city = forms.CharField(required=True, min_length=3, max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'Current city'}))
    country = forms.ModelChoiceField(required=True, queryset=Country.objects.all(), empty_label="Select Country",widget=forms.Select(attrs={'class': 'form-control'}))

