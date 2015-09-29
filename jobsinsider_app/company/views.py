from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login as login_session
from django.utils import timezone

from accounts import models as acc_mod
from core.decoraters import is_company
from accounts import forms as accountsform
from datetime import datetime
from urlparse import urlparse, parse_qs
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

    @method_decorator(login_required)
    @method_decorator(is_company)
    def post(self, request):
        """

        :param request:
        :return:
        """

class CompanyPassword(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        change_password = accountsform.ChangeProfilePassword()
        return render(request, 'company_change_password.html', {'cp': change_password})

    @method_decorator(login_required)
    @method_decorator(is_company)
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


class CompanyProfileView(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        user_basic = accountsform.UserForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username,


        })
        return render(request, 'company_profile.html', {'user_profile': user_basic})

    @method_decorator(login_required)
    @method_decorator(is_company)
    def post(self, request):
        """

        :param request:
        :return:
        """



class CompanyJobAd(View):
    """
    Adding user company advertisement
    """

    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        jobad = JobAdvertisementForm()
        return render(request, 'job_advertisement.html', {'job_form': jobad})

    def post(self, request):
        parameters = parse_qs(request.POST['form_val'])
        resp={}
        try:
            Advertisement(
                job_title=parameters['job_title'][0],
                job_position=parameters['job_position'][0],
                job_description=request.POST['description'],
                employment_id=parameters['employment'][0],
                experience_id=parameters['experience'][0],
                category_id=parameters['category'][0],
                country_id=parameters['country'][0],
                cities_id=parameters['cities'][0],
                salary_from=parameters['salary_from'][0],
                salary_to=parameters['salary_to'][0],
                degree_level_id=parameters['education'][0],
                submission_date=datetime.now(),
                company_user_id=request.user.id
            ).save()

            resp['status']= True    # when the query succeed.
            resp['last_inserted'] = Advertisement.admanager.latest('id').id

        except Exception as e:
            print e
            resp['status']= False   # In case if query fails

        return HttpResponse(json.dumps(resp))


class CompanyAdEdit(View):
    def get(self, request, job_id):
        """
        """
        try:
            data = Advertisement.admanager.filter(company_user_id=request.user.id, id=job_id).prefetch_related(
                'category'
            ).prefetch_related(
            'country'
            ).prefetch_related('cities')
            print data[0].category
            jobad = JobAdvertisementForm(initial={
                'job_title': data[0].job_title,
                'job_position':data[0].job_position,
                'job_description':data[0].job_description,
                'employment':data[0].employment_id,
                'experience':data[0].experience_id,
                'category':data[0].category_id,
                'country':data[0].country_id,
                'cities':data[0].cities_id,
                'salary_from':data[0].salary_from,
                'salary_to':data[0].salary_to,
                'education':data[0].degree_level_id,
                #submission_date=datetime.now(),
                #company_user_id=request.user.id

             }
            )

        except Exception as e:
            print e
            pass

        return render(request, 'job_advertisement_edit.html', {'job_form': jobad, 'jobid': job_id})
    def post(self, request, job_id):
        parameters = parse_qs(request.POST['form_val'])
        resp = {}
        Advertisement.admanager.filter(id=job_id, company_user_id=request.user.id).update(
                job_title=parameters['job_title'][0],
                job_position=parameters['job_position'][0],
                job_description=request.POST['description'],
                employment_id=parameters['employment'][0],
                experience_id=parameters['experience'][0],
                category_id=parameters['category'][0],
                country_id=parameters['country'][0],
                cities_id=parameters['cities'][0],
                salary_from=parameters['salary_from'][0],
                salary_to=parameters['salary_to'][0],
                degree_level_id=parameters['education'][0],
                # submission_date=datetime.now(),

            )

        resp['status']= True    # when the query succeed.



#Company settings for the job advert
class CompanyAdSettings(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request, last_id):
        return render(
            request,
            'job_advertisement_settings.html',
            {'last_id': last_id})

    def post(self, request, last_id):
        resp = {}
        try:
            if request.POST['date_value']:
                date_time = request.POST['date_value']
            else:
                date_time = None

            AdvertisementSettings(
                advertisement_id=last_id,
                is_apply_true=request.POST['is_apply_by'],
                apply_date=date_time,
                is_email=request.POST['is_email']
            ).save()

            resp['status']= True    # when the query succeed.

        except Exception as e:
            print e
            resp['status']= False

        return HttpResponse(json.dumps(resp))


class CompanyJobAdFinalize(View):
    """
    Your job application is in the review process
    """
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        return render(
            request,
            'review_job_advertisement.html'
        )

class Posted_jobs(View):
    """
    List all the posted jobs
    """
    @method_decorator(login_required)
    def get(self, request):
        list = Advertisement.admanager.posted(request.user.id)
        return render(request, 'posted_jobs.html', {'posted_jobs': list})


def delete_job(request, job_id):
    """
    Delete Job ID from the posted jobs
    """
    if request.method=='POST':
        resp={}
        try:
            AdvertisementSettings.objects.filter(advertisement_id=job_id).delete()
            Advertisement.admanager.filter(id=job_id).delete()
            resp['status']=True
        except:
            resp['status']= False
        return HttpResponse(json.dumps(resp))




class CompanyAdd(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        """

        :param request:
        :return:
        """


class Messages(View):
    @method_decorator(login_required)
    def get(self, request):
        print Advertisement.admanager.get_queryset()
        return render(request, 'company_message.html')