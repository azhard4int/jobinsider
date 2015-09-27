__author__ = 'azhar'
from django import forms
from models import *
from core import models as core_models
from redactor.widgets import RedactorEditor
from tinymce.widgets import TinyMCE

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

class JobAdvertisementForm(forms.ModelForm):

    experience = Experience.objects.all()
    choices_experience = [(ab.id, str(ab.experience_name)) for ab in experience]

    employment = Employment.objects.all()
    choices_employment = [(ab.id, str(ab.employment_name)) for ab in employment]


    education = core_models.Education.objects.all()
    choices_education = [(ab.id, str(ab.education_name)) for ab in education]


    categories = core_models.Categories.objects.all()
    choices_categories = [(ab.id, str(ab.category_name)) for ab in categories]


    countries = core_models.Countries.objects.all()
    choices_countries= [(ab.id, str(ab.country_name)) for ab in countries]


    job_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Company Industry',
            'class':'form-control',
        })
    )

    job_position = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'placeholder':'Total Positions',
            'class':'form-control',
        })
    )
    job_description = forms.CharField(
        # widget=RedactorEditor()
        widget=TinyMCE()
    )
    experience = forms.ChoiceField(
            choices=choices_experience,
            widget=forms.Select(
                attrs={
                    'class': 'experience_select_box form-control',

                }
            )
        )
    employment = forms.ChoiceField(
            choices=choices_employment,
            widget=forms.Select(
                attrs={
                    'class': 'employment_select_box form-control',

                }
            )
        )
    education = forms.ChoiceField(
            choices=choices_education,
            widget=forms.Select(
                attrs={
                    'class': 'education_select_box form-control',

                }
            )
        )
    category = forms.ChoiceField(
            choices=choices_categories,
            widget=forms.Select(
                attrs={
                    'class': 'category_select_box form-control',

                }
            )
        )
    country = forms.ChoiceField(
            choices=choices_countries,
            widget=forms.Select(
                attrs={
                    'class': 'countries_select_box form-control',

                }
            )
        )


    cities = forms.ChoiceField(
            widget=forms.Select(
                attrs={
                    'class': 'cities_select_box form-control',
                    'placeholder':'Select City',

                }
            )
    )

    salary_from = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
        })
    )
    salary_to = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
        })
    )
    # category = models.ForeignKey(core_models.Categories)
    # salary_from = models.BigIntegerField(
    #     default=10000
    # )
    # salary_to = models.BigIntegerField(
    #     default=10000
    # )
    # degree_level = models.ForeignKey(core_models.Education)

    class Meta:
        model = Advertisement
        fields = ['job_title', 'job_position', 'job_description']




