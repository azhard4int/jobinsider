from __future__ import absolute_import
import random
import string
import json
from datetime import timedelta


from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_ses, logout
from django.contrib.auth.decorators import login_required

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .forms import *
from .models import *
from django.utils import timezone
from django.views.generic import View
from django.core.mail import send_mail, EmailMultiAlternatives
from core import email
from users import models as usermodels



BASE_URL = 'http://127.0.0.1:8000'
STATUS_SUCCESS = 'Your account has been created successfully'
STATUS_EXIST = 'Account with that email address already exists.'
STATUS_WRONG = 'Invalid Username or Password'
STATUS_SENT = 'Please check your email address to reset password and follow the instructions on it.'
STATUS_NONE = 4 # 'There is no username exist with your entered username.'


def index(request):
    """

    """


def send_confirmation_email( **kwargs):

    sendemail_ = email.EmailFunc('activateaccount', **kwargs)
    sendemail_.generic_email()
    status = {'status': STATUS_SUCCESS}



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
            if result is True:
                error = {'status': STATUS_EXIST}

                return HttpResponse(
                    json.dumps(error),
                    content_type="application/json")

            else:
                user = user_form.save(commit=False)
                user.set_password(request.POST['password'])
                user.is_active = 0
                user.save()
                profile = userprofile_form.save(commit=False)
                profile.user = user
                profile.save()
                registered = True

                listvalue = {
                    'tosend': request.POST['email'],
                    'username': request.POST['username'],
                    'first_name': request.POST['first_name'],
                    'token': token_gen()
                }

                user_activation = UserActivation(
                    activation_key=listvalue['token'],
                    timestamp=timezone.now(),
                    user=user
                )
                user_activation.save()

                sendemail_ = email.EmailFunc('activateaccount', **listvalue)
                sendemail_.generic_email()
                status = {'status': STATUS_SUCCESS}
                return HttpResponseRedirect('/accounts/confirm-email/')
                # return HttpResponse(
                #     json.dumps(status),
                #     content_type="application/json")


    else:
        user_form = UserForm()
        userprofile_form = UserProfileForm()

    return render(request, 'register_account.html', {
        'user_form': user_form,
        'user_profile_form': userprofile_form,
        'registered': registered,
        'error': error
    })


def login_view(request):

    login = True
    error = None

    if request.user.is_active:
        return HttpResponseRedirect('/user/create-basic-profile/?step=0')
    else:
        if request.GET.get('error', ''):
            if request.GET.get('error') == 1:
                error = 'Your token time expired, please reset password once again.'

            if request.GET.get('error') == 2:
                error = 'Your Token already been used'
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is None:
                return HttpResponse(
                    json.dumps({'status': -1}),
                )

            if user:

                if user.is_superuser:   # For administrator privilleged user
                    login_ses(request, user)
                    return HttpResponse(json.dumps({'status': '1'}))

                if user.is_active:
                    login_ses(request, user)
                    return HttpResponse(json.dumps({
                        'status': 2}))
                else:
                    """
                        If the user account is not valid
                    """
                    login_ses(request, user)
                    return HttpResponse(json.dumps({
                        'status': 3}))
        else:
            login_form = LoginForm()
            # gotta work out for the error request up here.
            return render(request, 'login_account.html', {'login_form': login_form, 'error': error})


def forgot_password(request):
    # login = True
    error = None

    if request.method == 'POST':
        userdetail = request.POST['email']
        getuser = User.objects.filter(email=userdetail).exists()
        user_info = User.objects.filter(email=userdetail)
        if getuser is True:

            userdata = token_check(user_id=user_info[0].id)
            if userdata['usercheck'] is not None:
                exist = UserForgot.objects.filter(user_id=userdata['usercheck'][0].user_id).delete()
            username = User.objects.get(email=userdetail)
            token = token_gen()
            userforgot = UserForgot(
                token_key=token,
                timestamp=timezone.now(),
                token_status=0,
                user_id=int(username.id)
            )
            userforgot.save()

            listvalue = {
                'tosend': request.POST['email'],
                'username': username,
                'token': token
                }

            sendemail_ = email.EmailFunc('forgotpassword', **listvalue)
            sendemail_.generic_email()
            success = {'status': 1}

            return HttpResponse(
                json.dumps(success),
            )
        else:
            error = {'status': -1}  #'User email not found'
            return HttpResponse(
                json.dumps(error)
            )
    else:
        forgot = ForgotPassword()
        return render(request, 'forgot_password.html', {'forgotpassword': forgot})


def token_gen():
    return ''.join(random.choice(string.ascii_uppercase) for i in range(60))


def set_new_password(request):



    if request.method == 'POST':
        """
            If the request is of post data
        """
        print request.POST['password']
        user = User.objects.get(email=request.POST['email'])
        user.set_password(request.POST['password'])
        user.save()
        UserForgot.objects.filter(user_id=user.id).update(token_status=1)

        return HttpResponse(
            json.dumps(
                {
                    'status': 1
                }
            )
        )

    """
    To validate that the user token is valid or not!
    """
    tokenvalue = request.GET.get('pauthid', '')

    if tokenvalue is None or tokenvalue is '':  # first level - Token None.
        return HttpResponseRedirect(BASE_URL + '/accounts/login/')

    if tokenvalue is not None:  # second level Timestmap Checker
        userdetails = token_check(tokenvalue)
        if userdetails['usercheck'] is not None:   # if the user token is valid proceed.
                # if userdetails['timestamp_now'] > userdetails['timestamp_created']:   # 30 minutes timestamp.

                # Additional check if the token is already used!

                user_detail  = UserForgot.objects.filter(user_id=userdetails['usercheck'][0].user_id)
                if user_detail[0].token_status == 1:
                    return HttpResponseRedirect(BASE_URL + '/accounts/login/?error=2')  #  2 for already used token


                user_email = User.objects.filter(id=userdetails['usercheck'][0].user_id)[0].email
                setform = SetNewPassword(initial={'email': user_email})
                return render(request, 'set_password.html', {'setpassword': setform})

            # else:
            #     return HttpResponseRedirect(BASE_URL + '/accounts/login/?error=1')
        else:
            return HttpResponseRedirect(BASE_URL + '/accounts/login/')





def confirm_email(request):
    """
    To verify token and confirm the account.
    """

    user = request.user
    # print user
    # if user.is_active:
    token_value = request.GET.get('token', '')
    print token_value

    if len(token_value) > 10:
        try:
            user = UserActivation.objects.get(activation_key=token_value)
        except ObjectDoesNotExist:
            response = HttpResponse(json.dumps({'status': 'Invalid Activation Key'}))
            return response

        if user:    # If the user is already verified.
            if user.activation_status == 1:
                return HttpResponseRedirect('/user/create-basic-profile/?step=0')

        if user:
            user.activation_status = 1
            user.save()
            main_user = User.objects.get(id=user.user_id)
            main_user.is_active = 1
            main_user.save()



            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/accounts/confirm-email/')


def token_check(tokenvalue=None, user_id=None):     # bring the token.

    if tokenvalue is not None:
        usercheck = UserForgot.objects.filter(token_key=tokenvalue).prefetch_related('user')
    elif user_id is not None:
        usercheck = UserForgot.objects.filter(user_id=user_id).prefetch_related('user')
    try:
        timestamp_created = usercheck[0].timestamp
        timestamp_now = timezone.now() - timedelta(minutes=-30)
    except IndexError:
        usercheck = None
        timestamp_created = 0
        timestamp_now = 0
        pass
    details = {
        'usercheck': usercheck,
        'timestamp_created': timestamp_created,
        'timestamp_now': timestamp_now
    }
    return details


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('http://127.0.0.1:8000/accounts/login/')


def send_user_email(request):
    """
    This will be used to resend the confirmation emial to the user
    """
    try:
        userobj = UserActivation.objects.filter(user_id=request.user.id)
        if userobj:
            userToken = userobj[0].activation_key
            listvalue = {
                    'tosend': request.user.email,
                    'username': request.user.email,
                    'first_name': request.user.first_name,
                    'token': userToken
                }
            send_confirmation_email(**listvalue)
            return HttpResponse(json.dumps({'status':1}))


    except:
        pass


class ConfirmEmailView(View):
    """
        Confirm Your Email View Up here
    """
    def get(self, request):
        return render(request, 'confirm_email_view.html')