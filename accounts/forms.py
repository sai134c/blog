from django import forms
from django.contrib.auth.forms import UserCreationForm

class SighUpForm(UserCreationForm):
    email = forms.EmailField(max_length=128, required= True, help_text= 'Required')