__author__ = 'azhar'
from django import forms
from models import *

class CompanyProfileForm(forms.ModelForm):
    company_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Company Name',
            'class': 'form-control',
        })
    )
    your_role = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Your Role',
            'class':'form-control',
        })
    )
    company_intro = forms.Textarea()
    company_url = forms.URLField(
        widget=forms.TextInput(attrs={
            'placeholder':'Company Indusry',
            'class':'form-control',
        })
        )

    company_industry = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Company Indusry',
            'class':'form-control',
        })
    )

    class Meta:
        model = CompanyProfile
        fields = {
            'company_name',
            'your_role',
            'company_intro',
            'company_url',
            'company_industry'
        }