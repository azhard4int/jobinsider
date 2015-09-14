from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login as login_session


from accounts import models as acc_mod
from core.decoraters import is_company
from accounts import forms as accountsform
from forms import *
import simplejson as json


# Create your views here.

@login_required()
def index(request):
    return HttpResponseRedirect('/company/')



class Company_dashboard(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        user = acc_mod.UserProfile.objects.filter(user_id=request.user.id)[0]
        if user.company_profile_status==0:
            status = 0
        else:
            status = 1
        company_profile = CompanyProfileForm()
        return render(request, 'company_dashboard.html', {
            'body_status': status,
            'profile_form': company_profile
        })
    def post(self, request):
        CompanyProfile(
            company_name=request.POST['company_name'],
            your_role=request.POST['your_role'],
            company_intro=request.POST['company_intro'],
            company_url=request.POST['company_url'],
            company_industry =  request.POST['company_industry'],
            user_id = request.user.id
        ).save()
        user_update = acc_mod.UserProfile.objects.filter(
            user_id=request.user.id
        ).update(company_profile_status=1)


class CompanyListing(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        list = CompanyProfile.objects.filter(user_id=request.user.id)
        return render(request, 'companies.html', {'companies': list})


class CompanyPassword(View):
    @method_decorator(login_required)
    @method_decorator(is_company)


    def get(self, request):
        change_password = accountsform.ChangeProfilePassword()
        return render(request, 'user_change_password.html', {'cp': change_password})

    def post(self, request):
        if request.method=='POST':
            _check = User.objects.filter(id=request.user.id)
            print _check
            if _check:
                user = _check[0]
                if user.check_password(request.POST['password']):
                    if request.POST['new_password']==request.POST['confirm_new_password']:
                        user.set_password(request.POST['new_password'])
                        user.save()
                        login_session(request, user)
                        return HttpResponse(json.dumps({'status':1}))

                    else:
                        return HttpResponse(json.dumps({'status':-1}))
                else:
                    return HttpResponse(json.dumps({'status':-2}))
            else:
                return HttpResponse(json.dumps({'status':-3}))



class Posted_jobs(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'posted_jobs.html')

class Messages(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'company_message.html')