__author__ = 'azhar'
from models import User, UserProfile
from django import forms
from passwords.fields import PasswordField

class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        help_text='',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        help_text='',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name'
            }
        )
    )

    username = forms.CharField(
        help_text='',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Username'
            }
        ))
    email = forms.CharField(
        help_text='',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Email'
            }
        )
    )
    password = PasswordField(
        help_text='',
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password'
            }
        )
    )

    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'email', 'username', 'password'}

class UserProfileForm(forms.ModelForm):
    user_status = forms.ChoiceField(choices=(
        ('0', 'Job Seeker'),
        ('1', 'Company'),
    ), label='', help_text='')

    class Meta:
        model = UserProfile
        fields = {'user_status'}

class LoginForm(forms.ModelForm):
    username = forms.TextInput()
    password = PasswordField(
        help_text='',
        label='')

    class Meta:
        model = User
        fields = {'username', 'password'}


class ForgotPassword(forms.ModelForm):
    class Meta:
        model = User
        fields = {'email'}


class SetNewPassword(forms.ModelForm):
    password = PasswordField(
        widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Enter Your New Password'
        })
    )
    email = forms.TextInput()

    class Meta:
        model = User
        fields = {'email', 'password' }