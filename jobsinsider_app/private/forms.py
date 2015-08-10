__author__ = 'azhar'
from django import forms
from models import User

class Adminlogin(forms.ModelForm):
    username = forms.CharField()
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = {'username', 'password'}