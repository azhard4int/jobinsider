__author__ = 'azhar'
from django import forms

class Adminlogin(forms.ModelForm):
    username = forms.CharField()
    password= forms.PasswordInput

    class Meta:
        fields = {'username', 'password'}