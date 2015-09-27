__author__ = 'azhar'
from django import forms
from models import User
from core import models as modelf
from company import models as company_model

class Adminlogin(forms.ModelForm):
    username = forms.CharField()
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = {'username', 'password'}

class CategoryAdd(forms.ModelForm):
    category_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Category Name',
            'class':'form-control',
        })
    )
    category_status = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'placeholder':'Category Status',
            'class':'form-control',
        })
    )
    category_image = forms.ImageField

    class Meta:
        model = modelf.Categories
        fields = {'category_name', 'category_status', 'category_image'}


class CategoryEdit(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    category_name = forms.CharField()
    category_status = forms.IntegerField()

    class Meta:
        model = modelf.Categories
        fields = {'id', 'category_name', 'category_status'}

class AddSkill(forms.ModelForm):
    skill_name = forms.CharField()
    category_id = forms.IntegerField()

    class Meta:
        model = modelf.Skills
        fields = {'skill_name', 'category_id'}

class EditSkill(forms.ModelForm):
    skill_name = forms.CharField()
    skill_status = forms.IntegerField()
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = modelf.Skills
        fields = {'skill_name', 'id'}

class EducationForm(forms.ModelForm):
    education_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Education Type Name',
            'class':'form-control edu_text',
            'width': '500px'
        })
    )

    class Meta:
        model = modelf.Education
        fields = [
            'education_name',
        ]


class ExperienceForm(forms.ModelForm):
    experience_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Education Type Name',
            'class':'form-control edu_text',
            'width': '500px'
        })
    )

    class Meta:
        model = company_model.Experience
        fields = [
            'experience_name',
        ]


class EmploymentForm(forms.ModelForm):
    employment_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Employment Type Name',
            'class':'form-control edu_text',
            'width': '500px'
        })
    )

    class Meta:
        model = company_model.Employment
        fields = [
            'employment_name',
        ]