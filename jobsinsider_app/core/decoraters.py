__author__ = 'azhar'
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from accounts import models as acc_model


def is_company(func):
    def wrapper(request, *args, **kwargs):
        # print request.user
        user = acc_model.UserProfile.objects.filter(user_id=request.user.id)[0]
        if user.user_status==1:
            return func(request, *args, **kwargs)
        return HttpResponseRedirect('/user/dashboard')
    return wrapper



def is_job_seeker(func):
    def wrapper(request, *args, **kwargs):
        # print request.user
        user = acc_model.UserProfile.objects.filter(user_id=request.user.id)[0]
        if user.user_status==0:
            return func(request, *args, **kwargs)
        return HttpResponseRedirect('/company/index')
    return wrapper

def is_company_true(user_obj):
    user = acc_model.UserProfile.objects.filter(user_id=user_obj)[0]
    if user.user_status==1:
        # print 'here'
        return True
    else:
        return False

def is_jobseeker_true(user_obj):
    user = acc_model.UserProfile.objects.filter(user_id=user_obj)[0]
    if user.user_status==0:
        # print 'here'
        return True
    else:
        return False