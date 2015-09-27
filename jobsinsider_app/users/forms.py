__author__ = 'azhar'
from django import forms
from models import *
from core import models as core_model


class UserBioInfo(forms.ModelForm):
    choices = ((1,'Low',), (2,'Medium',), (3,'High',))
    user_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Title',
            'class': 'form-control'
            }
        )
    )
    user_overview = forms.Textarea(

    )
    user_language_pre = forms.ChoiceField(
        choices=choices
    )

    class Meta:
        model = UserBio
        fields = {
            'user_title',
            'user_overview',
            'user_bio_status',
            'user_portrait',
            'user_language_pre'
        }

class UserCVForm(forms.ModelForm):
    user_cv_file = forms.FileField(

    )
    class Meta:
        model = UserCV
        fields = {'user_cv_file'}


class UserLocationForm(forms.ModelForm):
    choices = ((1,'Low',), (2,'Medium',), (3,'High',))
    get_countries = core_model.Countries.objects.all()
    choices_countries = [(ab.id, str(ab.country_name)) for ab in get_countries]

    user_city = forms.ChoiceField(
        choices=choices,
        widget=forms.Select(
            attrs={
                'class': 'cities_select_box',

            }
        )
        )
    user_country = forms.ChoiceField(
        choices=choices_countries,
        widget=forms.Select(
            attrs={
                'class': 'countries_select_box',

            }
        )
    )
    user_address = forms.Textarea()
    user_zipcode  = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Zip Code'
        }
    ))
    user_phone_no = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Phone No'
        }
    ))

    class Meta:
        model = UserLocation
        fields = {
            'user_city',
            'user_country',
            'user_address',
            'user_zipcode',
            'user_phone_no'
        }

class UserEmploymentForm(forms.ModelForm):
    # listofyears = [print ab for ab in range(1950, 2015)]
    company_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Company Name'
    }))
    company_location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Company Location'
    }))
    company_worktitle = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Company Work Title'
    }))
    company_role = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Company Role'
    }))
    company_from = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control datepicker',
        'placeholder': 'Work From'

    }))
    company_to = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control datepicker',
        'placeholder': 'Work To'
    }))

    company_count = forms.CharField(widget=forms.HiddenInput(attrs={
        'value': '0'
    }))


    class Meta:
        model = UserEmployment
        fields = []


class EducationForm(forms.ModelForm):

    user_institute = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Institute Name'
    }))
    user_degree= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Degree Level'
    }))

    degree_from = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control datepicker',
        'placeholder': 'From'

    }))
    degree_to = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control datepicker',
        'placeholder': 'To'
    }))

    class Meta:
        model = UserEducation
        fields = {
            'user_institute',
            'user_degree',
            'degree_from',
            'degree_to'
        }


class InitialEmploymentForm(UserEmploymentForm):
    class Meta:
        model = UserEmployment
        fields = {
            # 'company_country'
            'company_name',
            'company_location',
            'company_worktitle',
            'company_role',
            'company_from',
            'company_to',
            'company_description',
            # 'company_count'
            }


class AddUserEmploymentForm(UserEmploymentForm):

    class Meta:
        model = UserEmployment
        # exclude = ['company_count', 'company_description']
        fields = {
            'company_name',
            'company_location',
            'company_worktitle',
            'company_role',
            'company_from',
            'company_to',
           }

