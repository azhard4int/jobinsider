from __future__ import absolute_import
import random
import string
import json


from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .forms import UserForm, UserProfileForm, LoginForm, ForgotPassword
from django.core.mail import send_mail, EmailMultiAlternatives
from core import email



STATUS_SUCCESS = 'Your account has been created successfully'
STATUS_EXIST = 'Account with that email address already exists.'
STATUS_WRONG = 'Invalid Username or Password'
STATUS_SENT = 'Please check your email address and follow the instructions on it.'
STATUS_NONE = 'Invalid Username or Password'

def index(request):
    """

    """


def register(request):
    """
    For registering the user based on their status.
    """
    registered = False
    error = None
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        userprofile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            print 'inside'
            result = User.objects.filter(email=request.POST['email']).exists()
            if result is True:
                error = {'status': STATUS_EXIST}

                return HttpResponse(
                    json.dumps(error),
                    content_type="application/json")

            else:
                user = user_form.save(commit=False)
                user.set_password(request.POST['password'])
                user.save()
                profile = userprofile_form.save(commit=False)
                profile.user = user
                profile.save()
                registered = True

                listvalue = {
                    'tosend': request.POST['email'],
                    'username': request.POST['username'],
                }

                sendemail_ = email.EmailFunc('activateaccount', **listvalue)
                sendemail_.generic_email()
                status = {'status': STATUS_SUCCESS}
                return HttpResponse(
                    json.dumps(status),
                    content_type="application/json")

    else:
        user_form = UserForm()
        userprofile_form = UserProfileForm()

    return render(request, 'register_account.html', {
        'user_form': user_form,
        'user_profile_form': userprofile_form,
        'registered': registered,
        'error': error
    })

def login(request):

    login = True
    error =None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse(
                json.dumps({'status':STATUS_NONE}),
                content_type="application/json"
            )
        if user:
            if user.is_active:
                return HttpResponseRedirect('http://google.com')
            else:
                return HttpResponseRedirect('http://facebook.com')
    else:
        login_form = LoginForm()
        return render(request, 'login_account.html', {'login_form':login_form})

def forgot_password(request):
    login = True
    error = None

    if request.method == 'POST':
        userdetail = request.POST['email']
        getuser = User.objects.filter(email=userdetail).exists()
        print getuser
        if getuser is True:
            token = token_gen()
            try:
                listvalue = {
                    'tosend': request.POST['email'],
                    'username': request.POST['username'],
                    'token': token
                }
                sendemail_ = email.EmailFunc('forgotpassword', **listvalue)
                sendemail_.generic_email()
            except:
                pass

        else:
            error = {'status': 'User email not found'}
            return HttpResponse(
                json.dumps(error),
                content_type="application/json")
    else:
        forgot = ForgotPassword()
        return render(request, 'forgot_password.html', {'forgotpassword': forgot})


def token_gen():
    return (''.join(random.choice(string.ascii_uppercase) for i in range(60)))

def set_token_forgot(tokenvalue, uservalue):

    """

    :param tokenvalue:
    :param uservalue:
    :return:
    """