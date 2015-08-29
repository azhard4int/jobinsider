__author__ = 'azhar'
from django import forms
from models import User
from core import models as modelf


class Adminlogin(forms.ModelForm):
    username = forms.CharField()
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = {'username', 'password'}

class CategoryAdd(forms.ModelForm):
    category_name = forms.CharField()
    category_status = forms.IntegerField()
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