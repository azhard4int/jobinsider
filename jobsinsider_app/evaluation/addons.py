__author__ = 'v'
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login as login_session
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login
from django.core import serializers
from accounts import models as acc_mod
from core.decoraters import is_company
from accounts import forms as accountsform
from datetime import datetime
from urlparse import urlparse, parse_qs
import models
import simplejson as json

def getevaluation(id):
        data = models.evaluation_test_template.object.get(id=id)
        whole = {
               'evaluation_name':data.evaluation_name,
               'evaluation_catagory':data.evaluation_catagory,
               'evaluation_status':data.status,
               'evaluation_type':data.type,
               'evaluation_total_questions':data.evaluation_questions
           }
        return data