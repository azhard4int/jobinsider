from django.shortcuts import render
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string


# Create your views here.
from django.shortcuts import *
from django.views.generic import View
from datetime import datetime
from models import *
from core import models as core_models
from accounts import models as accounts_models
from company import models as company_models
from company import views as company_views
from users import models as users_models
from user_agents import parse


import os
import sys
import IP2Location
import logging
import simplejson as json

def build_template(request, ajax,job_advertisement, filtered_results, is_favorite_job=None, is_job_applied=None, list=None):
    user_status = None
    obj = SearchView()
    is_user_company = None
    body_status = 0
    try:
        if request.user.id:
            body_status = company_views.is_body_status(request)
            user_status = obj.is_user_job_seeker(request.user.id)
            user_company = obj.is_user_company(request.user.id)
            if user_company == 1:
                is_user_company = 1
            print "body status is {0}".format(body_status)
    except Exception as IndexError:
        user_status = 1
        print IndexError
        pass
    if is_favorite_job:
        #if this is the favorite page request
        if ajax == '1':
            html = render_to_string('jobs_favorite_view.html', {
                'data':job_advertisement,
                'user_status': user_status,
                'company_status': is_user_company,
                'filtered_results': filtered_results
                })
            return HttpResponse(html)
        else:

            return render(request, 'jobs_favorite.html', {
                'data':job_advertisement,
                'user_status': user_status,
                'filtered_results': filtered_results,
                'body_status': body_status # Taking the function from company views
            })
    elif is_job_applied:
        if ajax == '1':
            html = render_to_string('jobs_applied_view.html', {
                'data':job_advertisement,
                'user_status': user_status,
                'company_status': is_user_company,
                'filtered_results': filtered_results
                })
            return HttpResponse(html)
        else:
            return render(request, 'jobs_applied.html', {
                'data':job_advertisement,
                'user_status': user_status,
                'company_status': is_user_company,
                'filtered_results': filtered_results,
                'body_status': body_status # Taking the function from company views
            })
    else:
        if ajax == '1':
            print list
            html = render_to_string('jobs_view.html', {
                'data': job_advertisement,
                'user_status': user_status,
                'company_status': is_user_company,
                'filtered_results': filtered_results,
                'data_attributes': list
                })
            return HttpResponse(html)
        else:
            return render(request, 'index.html', {
                'data': job_advertisement,
                'user_status': user_status,
                'company_status': is_user_company,
                'filtered_results': filtered_results,
                'body_status': body_status # Taking the function from company views
            })


class Default_Search(View):
    def get(self, request):
        obj = SearchView()
        list_all = obj.fetch_all_adverts()
        page = request.GET.get('page')
        ajax = request.GET.get('is_ajax')
        job_advertisement = obj.paginate_data(list_all, page)
        return build_template(request,ajax,job_advertisement, filtered_results=0)

#to get filtered based results.
def filtered_results(request):
    """
    """
    obj = SearchView()
    list = obj.fetch_filtered_adverts(
        category=request.GET.get('categories'),
        experience=request.GET.get('experience'),
        education=request.GET.get('education'),
        employment=request.GET.get('employment'),
        keyword=request.GET.get('search'),
    )
    data_list = {
        'categories': request.GET.get('categories'),
        'experience': request.GET.get('experience'),
        'education': request.GET.get('education'),
        'employment': request.GET.get('employment'),

    }
    page = request.GET.get('page')
    ajax = request.GET.get('is_ajax')
    job_advertisement = obj.paginate_data(list, page)
    return build_template(request,ajax,job_advertisement, filtered_results=1, list=data_list)


class Favorite_Job(View):
    """
    Favorite Jobs Advertisement List
    """
    def get(self, request):
        """
        """
        obj = SearchView()
        list_all = obj.get_favorite_jobs(request.user.id)
        page = request.GET.get('page')
        ajax = request.GET.get('is_ajax')
        job_advertisement = obj.paginate_data(list_all, page)
        return build_template(request,ajax,job_advertisement, filtered_results=0, is_favorite_job=True)

    def post(self, request):
        """

        :param request:
        :return:
        """

class Applied_Job(View):
    """
    Favorite Jobs Advertisement List
    """
    def get(self, request):
        """
        """
        obj = SearchView()
        list_all = obj.get_applied_jobs(request.user.id)
        page = request.GET.get('page')
        ajax = request.GET.get('is_ajax')
        job_advertisement = obj.paginate_data(list_all, page)
        return build_template(request,ajax,job_advertisement, filtered_results=0, is_job_applied=True)

    def post(self, request):
        """

        :param request:
        :return:
        """


class Job_Details(View):
    """
    Detailed job page view
    """
    def get(self, request, job_id):
        data_obj = SearchView()
        data = data_obj.fetch_job_details(job_id)
        is_applied = data_obj.is_already_applied(request.user.id, job_id)
        is_favorite = data_obj.is_already_favorite(request.user.id, job_id)
        is_favorite_status = False
        is_applied_status = False
        if is_applied:
            is_applied_status = True
        if is_favorite:
            is_favorite_status = True
        is_company = False
        if accounts_models.UserProfile.objects.filter(user_id=request.user.id)[0].user_status == 1:
            is_company = True

        company = data_obj.fetch_company_details(data.company_user_id)

        # Getting current visitors
        data_main = self.parse_visitor_info(request)

        get_current_visitor = 0
        self.save_visitors(request, job_id, data_main, get_current_visitor, 0)
        # if get_current_visitor:
        return render(request, 'jobs_detail.html', {
            'job': data,
            'company':company,
            'user_status':request.user.id,
            'is_applied': is_applied_status,
            'is_company': is_company,
            'is_favorite': is_favorite_status,
            'body_status': company_views.is_body_status(request)
        })

    def post(self, request, job_id):
        """
        """
        evaluation_score = None
        try:
            evaluation_score = request.POST['evaluation_score']
        except Exception as e:
            pass
        company_models.AdvertisementApplied(
            user_id = request.user.id,
            advertisement_id = job_id,
            applied_date = datetime.now(),
            evaluation_test_score = (evaluation_score)
        ).save()
        # increment the value of the job advertisement
        total_count = company_models.Advertisement.admanager.applied_user(job_id)
        company_models.Advertisement.admanager.is_total_applied(job_id, total_count)
        return HttpResponse(
            json.dumps({
                'status': True,
                'response': 'Job Applying Done Successfully!'
            })
        )

    def parse_visitor_info(self, request):
        # Extracting meaningful data from the visitor request

        user_agent = parse(request.META['HTTP_USER_AGENT'])
        # data = parse(ua_string)
        data = {}
        # Accessing user agent's browser attributes
        data['browser'] = user_agent.browser # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
        data['user_agent_family'] = user_agent.browser.family # returns 'Mobile Safari'
        data['user_agent_version'] = user_agent.browser.version # returns (5, 1)
        data['version_string'] = user_agent.browser.version_string # returns '5.1'

        # Accessing user agent's operating system properties
        data['os'] = user_agent.os # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
        data['os_family'] = user_agent.os.family # returns 'iOS'
        data['os_version'] = user_agent.os.version # returns (5, 1)
        data['os_string'] = user_agent.os.version_string # returns '5.1'

        # Accessing user agent's device properties
        data['device'] = user_agent.device # returns Device(family=u'iPhone', brand=u'Apple', model=u'iPhone')
        data['device_family'] = user_agent.device.family # returns 'iPhone'
        data['device_brand'] = user_agent.device.brand # returns 'Apple'
        data['device_model'] = user_agent.device.model # returns 'iPhone'

        # Getting user referral
        # data['referral'] = request.META['HTTP_REFERER']

        # Getting user IP Address
        data['remote_address'] = request.META['REMOTE_ADDR']

        # Getting Visitor Country Through Ip2location
        IP2LocObj = IP2Location.IP2Location()

        IP2LocObj.open(os.getcwd() + "/jobs/data/IP-COUNTRY.BIN")
        rec = IP2LocObj.get_all("39.32.240.193")
        data['country_short'] = rec.country_short
        data['country_long'] = rec.country_long
        return data

    def save_visitors(self, request, job_id, data, get_current_visitor, status=0):
        try:
            gender_status = users_models.UserBio.objects.filter(
                user_id=request.user.id
            )[0].user_gender
        except:
            gender_status=2
            pass

        analytics_version = company_models.AdvertisementAnalytics(
            advertisement_id=job_id,
            user_agent=request.META['HTTP_USER_AGENT'],
            user_agent_family=data['user_agent_family'],
            user_agent_version=data['version_string'],
            remote_address=data['remote_address'],
            os_family=data['os_family'],
            os_version=data['os_string'],
            total_visitors=int(get_current_visitor),
            unique_visitors=0,
            is_gender=0,
            post_date =datetime.now(),
            country_short = data['country_short'],
            country_long = data['country_long'],
            visitor_gender=gender_status
        ).save()



def add_favorite_job(request):
    data_obj = SearchView()
    try:
        company_models.AdvertisementFavorite(
                user_id = request.user.id,
                advertisement_id = request.POST['job_id'],
                add_date = datetime.now()
            ).save()
    except:
        return HttpResponse(json.dumps({'status': False, 'response': 'Job Already Exist in Favorites!'}))
    return HttpResponse(
            json.dumps({
                'status': True,
                'response': 'Job Has Been Added to Favorite!'
            })
        )
def remove_favorite_job(request):
    data_obj = SearchView()
    company_models.AdvertisementFavorite.objects.filter(
        user_id=request.user.id,
        advertisement_id=request.POST['job_id']).delete()
    return HttpResponse(
            json.dumps({
                'status': True,
                'response': 'Job Deleted Successfully!'
            })
        )