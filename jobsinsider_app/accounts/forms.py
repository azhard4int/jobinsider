__author__ = 'azhar'
from models import User, UserProfile
from django import forms
from passwords.fields import PasswordField

class UserForm(forms.ModelForm):
    """
        User Account Creation Form
    """
    first_name = forms.CharField(
        help_text='',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-control'
            }
        )
    )
    last_name = forms.CharField(
        help_text='',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'form-control'
            }
        )
    )

    username = forms.CharField(
        help_text='',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Username',
                'class': 'form-control'

            }
        ))
    email = forms.CharField(
        help_text='',
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter Email',
                'class': 'form-control'

            }
        )
    )
    password = PasswordField(
        help_text='',
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password',
                'class': 'form-control'

            }
        )
    )

    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'email', 'username', 'password'}

class UserProfileForm(forms.ModelForm):
    """
       Specifically for the user selection either job seeker or company
    """
    user_status = forms.ChoiceField(choices=(
        ('0', 'Job Seeker'),
        ('1', 'Company'),
    ), label='', help_text='')


    # user_status = forms.ChoiceField(widget=forms.RadioSelect, choices=(
    #     ('0', 'Job Seeker'),
    #     ('1', 'Company'),
    # ), label='', help_text='')

    class Meta:
        model = UserProfile
        fields = {'user_status'}

class LoginForm(forms.ModelForm):
    """
       Specifically for the login form
    """
    username = forms.CharField(
        help_text='',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Username',
                'class': 'form-control'

            }
        ))
    password = PasswordField(
        help_text='',
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password',
                'class': 'form-control'

            }
        )
    )


    class Meta:
        model = User
        fields = {'username', 'password'}


class ForgotPassword(forms.ModelForm):
    email = forms.CharField(
        help_text='',
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter Your Email Address',
                'class': 'form-control'

            }
        ))
    class Meta:
        model = User
        fields = {'email'}


class SetNewPassword(forms.ModelForm):
    password = PasswordField(
        widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Enter Your New Password',
            'class': 'form-control'

        })
    )
    email = forms.CharField(
        help_text='',
        label='',
        widget=forms.EmailInput(
        attrs={
            'placeholder': 'Enter Your Email',
            'class': 'form-control'

        }
    ))

    class Meta:
        model = User
        fields = {'email', 'password' }