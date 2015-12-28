__author__ = 'azhar'
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts import models as accounts_models
from company import models as company_models

import simplejson as json


def homepage(request):
    total_companies = accounts_models.UserProfile.objects.filter(company_profile_status=1).count()
    total_jobseekers = accounts_models.UserProfile.objects.filter(company_profile_status=0).count()
    jobs_posted = company_models.Advertisement.admanager.all().count()
    return render(request, 'homepage/index.html', {
        'total_companies': total_companies,'total_jobseekers': total_jobseekers, 'jobs_posted': jobs_posted})

    # return render(request, 'homepage.html')

@login_required(login_url='/accounts/login/')
def dashboard(request):

    return render(request, 'dashboard.html')
