import smtplib
import random
import string
import json

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from forms import UserForm, UserProfileForm, LoginForm, ForgotPassword
from django.core.mail import send_mail


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
            result = User.objects.filter(email=request.POST['email']).exists()
            print result
            if result is True:
                error = "Account with that email address already exists"
            else:
                user = user_form.save(commit=False)
                user.set_password(request.POST['password'])
                user.save()
                profile = userprofile_form.save(commit=False)
                profile.user = user
                profile.save()
                registered = True

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
        print user
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
            token = (''.join(random.choice(string.ascii_uppercase) for i in range(60)))
            send_mail('Subject here', 'Here is the message.{0}'.format(token), 'waqar@techpointmedia.com',
             ['azhar@d4int.com'], fail_silently=False)

        else:
            error = {'status': 'User email not found'}
            return HttpResponse(
                json.dumps(error),
                content_type="application/json")
    else:
        forgot = ForgotPassword()
        return render(request, 'forgot_password.html', {'forgotpassword': forgot})