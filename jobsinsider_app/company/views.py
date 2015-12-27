from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login as login_session
from django.utils import timezone
from django.db.models import Count, Prefetch
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts import models as acc_mod
from core.decoraters import is_company
from accounts import forms as accountsform
from datetime import datetime, timedelta
from urlparse import urlparse, parse_qs
from user_agents import parse
from forms import *
from itertools import chain
from core import email
from models import AppliedCandidatesFilter

import simplejson as json
import sys
import os


# Create your views here.

@login_required()
def index(request):
    return HttpResponseRedirect('/company/')

def is_body_status(request):
    user = acc_mod.UserProfile.objects.filter(user_id=request.user.id)[0]
    if user.company_profile_status == 0:
        status = 0
    else:
        status = 1
    return status

class Company_dashboard(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        status = is_body_status(request)
        company_profile = CompanyProfileForm()
        posted_jobs = Advertisement.admanager.filter(company_user_id=request.user.id).count()
        total_applications = AdvertisementApplied.objects.filter(
            advertisement=Advertisement.admanager.filter(company_user_id=request.user.id),
        ).count()
        jobs_details = Advertisement.admanager.posted(request.user.id).order_by('-submission_date')[:5]
        schedule_interviews = ShortlistedCandidates.objects.filter(
            advertisement__company_user_id=request.user.id,
            is_interview=1
        ).prefetch_related('advertisement')
        total_shortlisted = ShortlistedCandidates.objects.filter(
            advertisement__company_user_id=request.user.id
        ).prefetch_related('advertisement').count()
        total_shortlisted_interview = ShortlistedCandidates.objects.filter(
            advertisement__company_user_id=request.user.id,
            is_interview=1
        ).prefetch_related('advertisement').count()

        notification = Notification.objects.filter(user_id=request.user.id).order_by('-id')[:3]

        return render(request, 'company_dashboard.html', {
            'body_status': status,
            'profile_form': company_profile,
            'posted_jobs': posted_jobs,
            'job_details': jobs_details,
            'total_applications': total_applications,
            'total_schedule': schedule_interviews,
            'total_shortlisted': total_shortlisted,
            'total_shortlisted_interview': total_shortlisted_interview,
            'user_is_company': True,
            'notification':notification
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
        return HttpResponse(
            json.dumps(
                {
                    'status': True
                }
            )
        )


class ShortlistedCandidatesDate(View):
    def post(self, request):
        print request.POST
        if request.POST['scheduled_date'] == '':
            return HttpResponse(json.dumps({'status': False,'errors':True}))

        date_from = datetime.strptime(request.POST['scheduled_date'], '%Y-%m-%d') - timedelta(days=1)
        date_to = datetime.strptime(request.POST['scheduled_date'], '%Y-%m-%d') + timedelta(days=1)
        schedule_interviews = ShortlistedCandidates.objects.filter(
            advertisement__company_user_id=request.user.id, shortlisted_date__range = [date_from, date_to]
        ).prefetch_related('advertisement')
        #shortlisted_date__gt =
        html = render_to_string('schedule_interviews_date.html', {'total_schedule': schedule_interviews})
        return HttpResponse(json.dumps({'status':True, 'html':html}))


class CompanyListing(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        list = CompanyProfile.objects.filter(user_id=request.user.id)
        return render(request, 'companies.html', {'companies': list, 'user_is_company': True,
                                                  'body_status': is_body_status(request)})

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
        return render(request, 'company_change_password.html', {'cp': change_password, 'user_is_company': True,
                                                                'body_status': is_body_status(request)})

    @method_decorator(login_required)
    @method_decorator(is_company)
    def post(self, request):
        if request.method=='POST':
            _check = User.objects.filter(id=request.user.id)
            print _check
            if _check:
                user = _check[0]
                if user.check_password(request.POST['password']):
                    if request.POST['new_password'] == request.POST['confirm_new_password']:
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
        return render(request, 'company_profile.html', {'user_profile': user_basic, 'user_is_company': True})

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
        status  = is_body_status(request)
        return render(
            request,
            'job_advertisement.html',
            {
                'job_form': jobad,
                'body_status': status,
                'user_is_company': True
            }
        )

    def post(self, request):
        parameters = parse_qs(request.POST['form_val'])
        resp = {}
        try:
            get_company_name = CompanyProfile.objects.filter(
                user_id=request.user.id
            )[0].company_name
            if request.POST['evaluation_id'] == '0':
                #This is for the non evaluation id
                Advertisement(
                    salary_currency=request.POST['salary_currency'],
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
                    company_user_id=request.user.id,
                    company = get_company_name,
                    is_evaluation_test=False
                ).save()
            else:
                #This is for the evaluation id
                evaluation_id = request.POST['evaluation_id']
                Advertisement(
                    salary_currency=request.POST['salary_currency'],
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
                    company_user_id=request.user.id,
                    company = get_company_name,
                    evaluation_test_id=evaluation_id,
                    is_evaluation_test=True

                ).save()

            resp['status']= True    # when the query succeed.
            resp['last_inserted'] = Advertisement.admanager.latest('id').id
            # Advertisement.admanager.filter(id=resp['last_inserted']).update(
            #     salary_currency=request.POST['salary_currency'],
            # )

        except Exception as e:
            print e
            resp['status']= False   # In case if query fails

        return HttpResponse(json.dumps(resp))

class CompanyAdEdit(View):
    def get(self, request, job_id):
        try:
            data = Advertisement.admanager.filter(company_user_id=request.user.id, id=job_id).prefetch_related(
                'category'
            ).prefetch_related(
            'country'
            ).prefetch_related('cities').prefetch_related('evaluation_test')
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
        status = is_body_status(request)
        return render(request, 'job_advertisement_edit.html', {
            'job_form': jobad,
            'jobid': job_id,
            'job_approval_status': data[0].job_approval_status,
            'body_status': status,
            'evaluation_test_status': data[0].evaluation_test_id,
            'evaluation': data[0].evaluation_test_id,
            'user_is_company': True
        })
    def post(self, request, job_id):
        parameters = parse_qs(request.POST['form_val'])
        resp = {}
        if request.POST['evaluation_id'] == '0':
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
                    salary_currency=parameters['salary_currency'][0],
                    degree_level_id=parameters['education'][0],
                    is_evaluation_test=False
                    # submission_date=datetime.now(),
                    )
        else:
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
                    salary_currency=parameters['salary_currency'][0],
                    degree_level_id=parameters['education'][0],
                    evaluation_test_id=request.POST['evaluation_id'],
                    is_evaluation_test=True
                    # submission_date=datetime.now(),
                    )
        resp['status']= True    # when the query succeed.
        return HttpResponse(json.dumps(resp))

#Company settings for the job advert
class CompanyAdSettings(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request, last_id):
        status = is_body_status(request)
        return render(
            request,
            'job_advertisement_settings.html',
            {
                'last_id': last_id,
                'body_status': status,
                'user_is_company': True
            }
        )

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
            'review_job_advertisement.html',
            {
                'body_status': is_body_status(request),
                'user_is_company': True
             }
        )


class CompanyEvaluation(View):
    def post(self, request):
        evaluation = evaluation_models.evaluation_test_template.objects.filter(
            user_id=request.user.id,evaluation_status=1)
        return HttpResponse(serializers.serialize('json', evaluation))


class Posted_jobs(View):
    """
    List all the posted jobs
    """
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        list = Advertisement.admanager.posted(request.user.id)
        return render(
            request,
            'posted_jobs.html',
            {
                'posted_jobs': list,
                'body_status': is_body_status(request),
                'user_is_company': True
            }
        )

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


def pause_job(request, job_id):
    """
    Delete Job ID from the posted jobs
    """
    if request.method=='POST':
        resp={}
        try:
            Advertisement.admanager.filter(id=job_id).update(
                job_approval_status=3
            )
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

class MessagesView(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request):
        print "omer MessagesView"
        list_users = Messages.objects.raw(
            """
             SELECT * from company_messages join auth_user ON auth_user.id = company_messages.receiver_id
             where sender_id={0}
             group by auth_user.id order by company_messages.date_send
            """.format(request.user.id)
        )




        # print list_users[0].message_body
        try:
            print list_users[0] # To check if the user exists or not
        except IndexError:
            return render(request, 'company_message_none.html', {'user_is_company': True})

        data = get_messages(list_users[0].receiver_id,request.user.id)
        print data
        return render(
            request,
            'company_message.html',
            {
                'list': list_users,
                'message_data': data['all_data_sort'],
                'sender_side_name': data['server_side_name'],
                'sender_id': request.user.id,
                'candidate_id': list_users[0].receiver_id,
                'user_is_company': True,
                'body_status': is_body_status(request)

            }
        )

    def post(self, request):
        data = []
        try:
            data = get_messages(request.POST['candidate_id'],request.user.id)
        except IndexError:
            return HttpResponse(json.dumps({'success': False}))
        html =  render_to_string('company_message_dynamic.html', {
            'message_data': data['all_data_sort'],
            'sender_side_name': data['server_side_name'],
            'sender_id': request.user.id,
            'user_is_company': True
        })
        return HttpResponse(html)



def get_messages(candidate_id, user_id):
        data_sender_side = Messages.objects.filter(
            sender_id=user_id,
            receiver_id=candidate_id
        ).prefetch_related(
            'sender'
        ).order_by('date_send') #Sender messages to the receiver
        print data_sender_side
        data_receiver_side = Messages.objects.filter(
            sender_id=candidate_id,
            receiver_id=user_id
        ).prefetch_related(
            'receiver'
        ).order_by('date_send') # Which receiver sends the message to the sender
        print data_receiver_side
        # merging the two models instances
        if data_receiver_side:
            all_data_sort = sorted(chain(data_sender_side, data_receiver_side),
                                   key=lambda message_data: message_data.date_send, reverse=False)
        else:
            all_data_sort = sorted(data_sender_side, key=lambda message_data: message_data.date_send, reverse=False)
        # receiver sending the message to the sender.
        sender_side_name = data_sender_side[0].receiver.first_name + " " + data_sender_side[0].receiver.last_name
        data_value = {
            'all_data_sort': all_data_sort,
            'server_side_name': sender_side_name
        }
        return data_value


class AppliedCandidates(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request, job_id):
        data = AdvertisementApplied.objects.raw(
            """
            SELECT *
            FROM company_advertisementapplied join users_userlocation on users_userlocation.user_id=company_advertisementapplied.user_id
            join users_userbio on users_userbio.user_id=company_advertisementapplied.user_id join  users_usereducation on
            users_usereducation.user_id = company_advertisementapplied.user_id join users_useremployment on
            users_useremployment.user_id = company_advertisementapplied.user_id join auth_user
            on auth_user.id = company_advertisementapplied.user_id join core_cities on users_userlocation.user_city_id = core_cities.id
            join core_countries on users_userlocation.user_country_id = core_countries.id left outer join
            evaluation_evaluation_result on evaluation_evaluation_result.user_id = company_advertisementapplied.user_id
            where advertisement_id={0} and company_advertisementapplied.candidate_status=TRUE group by auth_user.id
            """.format(job_id)

        )
        user_employment = AdvertisementApplied.objects.raw(
            """
            SELECT * FROM company_advertisementapplied join users_useremployment on users_useremployment.user_id = company_advertisementapplied.user_id
            where advertisement_id={0} and company_advertisementapplied.candidate_status=TRUE

            """.format(job_id)
        )
        user_education =  AdvertisementApplied.objects.raw("""
            SELECT * FROM company_advertisementapplied join users_usereducation on users_usereducation .user_id = company_advertisementapplied.user_id
            where advertisement_id={0} and company_advertisementapplied.candidate_status=TRUE""".format(job_id)
        )
        # Previous one

        """
        applied_country_users = AdvertisementApplied.objects.raw(""" """
        SELECT count(country_name) as total_per_country, company_advertisementapplied.id,  country_name, company_advertisement.country_id as country_value FROM company_advertisementapplied join
        company_advertisement on company_advertisementapplied.advertisement_id=company_advertisement.id
        join core_countries on core_countries.id = company_advertisement.country_id where
        company_advertisementapplied.advertisement_id={0} group by country_name"""""".format(job_id))
        """

        applied_country_users = AdvertisementApplied.objects.raw("""
        SELECT count(country_name) as total_per_country, company_advertisementapplied.id,  country_name,
        users_userlocation.user_country_id as country_value FROM company_advertisementapplied join users_userlocation
        on company_advertisementapplied.user_id=users_userlocation.user_id join core_countries on
        users_userlocation.user_country_id = core_countries.id where company_advertisementapplied.advertisement_id={0}
        and company_advertisementapplied.candidate_status=TRUE group by country_name""".format(job_id))

        # Previous one
        """
          SELECT company_advertisementapplied.id, count(*) as total_per_city, city_name,company_advertisement.cities_id
           as city_value, country_name FROM company_advertisementapplied join company_advertisement on
            company_advertisementapplied.advertisement_id=company_advertisement.id join core_countries on
            core_countries.id = company_advertisement.country_id join core_cities on
            core_cities.id = company_advertisement.cities_id where company_advertisementapplied.advertisement_id={0}
            group by city_name"""


        applied_cities_users = AdvertisementApplied.objects.raw(
            """
            SELECT company_advertisementapplied.id, count(*) as total_per_city, city_name,users_userlocation.user_city_id
            as city_value, country_name FROM company_advertisementapplied join users_userlocation on
            company_advertisementapplied.user_id=users_userlocation.user_id join core_countries on
            users_userlocation.user_country_id = core_countries.id join core_cities on
            users_userlocation.user_city_id = core_cities.id where company_advertisementapplied.advertisement_id={0} and
            company_advertisementapplied.candidate_status=TRUE group by city_name
            """.format(job_id)
        )
        applied_gender_users = AdvertisementApplied.objects.raw(
            """
            SELECT count(*) as type, user_gender, company_advertisementapplied.id  FROM `company_advertisementapplied` join users_userbio on
            company_advertisementapplied.user_id = users_userbio.user_id where company_advertisementapplied.advertisement_id = {0}
            and company_advertisementapplied.candidate_status=TRUE group by user_gender
            """.format(job_id)
        )

        is_evaluation_test = Advertisement.admanager.filter(id=job_id)[0].is_evaluation_test
        list_total = int(len(list(data)))
        print list_total
        return render(request, 'applied_candidates.html', {
            'data': data,
            'employment': user_employment,
            'education': user_education,
            'job_id': job_id,
            'data_count': list_total,
            'applied_country_user': applied_country_users,
            'applied_cities_user': applied_cities_users,
            'applied_gender_user': applied_gender_users,
            'user_is_company': True,
            'is_evaluation_test': is_evaluation_test,
            'body_status': is_body_status(request)
        })


def applied_country(request):
    if request.method == 'POST':
        applied = AppliedCandidatesFilter(request.POST['job_id'], country_id=request.POST['country_id'])
        html = render_to_string('applied_candidate_dynamic.html', {
            'data': applied.candidates_list(),
            'education': applied.candidates_education(),
            'employment': applied.candidates_employment(),
            'is_evaluation_test': Advertisement.admanager.filter(id=request.POST['job_id'])[0].is_evaluation_test

        }, context_instance=RequestContext(request))
        return HttpResponse(html)


def applied_city(request):
    if request.method == 'POST':
        applied = AppliedCandidatesFilter(request.POST['job_id'],city_id=request.POST['city_id'])
        html = render_to_string('applied_candidate_dynamic.html', {
            'data': applied.candidates_list(),
            'education': applied.candidates_education(),
            'employment': applied.candidates_employment(),
            'is_evaluation_test': Advertisement.admanager.filter(id=request.POST['job_id'])[0].is_evaluation_test
        }, context_instance=RequestContext(request))
        return HttpResponse(html)

def applied_gender(request):
    if request.method == 'POST':
        applied = AppliedCandidatesFilter(request.POST['job_id'],gender=request.POST['gender'])
        html = render_to_string('applied_candidate_dynamic.html', {
            'data': applied.candidates_list(),
            'education': applied.candidates_education(),
            'employment': applied.candidates_employment(),
            'is_evaluation_test': Advertisement.admanager.filter(id=request.POST['job_id'])[0].is_evaluation_test
        }, context_instance=RequestContext(request))
        return HttpResponse(html)

class Shortlisted(View):
    def post(self, request, candidate_id, job_id ):
        ShortlistedCandidates(
            user_id=candidate_id,
            advertisement_id=job_id,
            shortlisted_date=datetime.now()
        ).save()

        AdvertisementApplied.objects.filter(
            user_id=candidate_id,
            advertisement_id=job_id
        ).update(
            is_shortlisted=True
        )
        return HttpResponse(json.dumps({
            'status': True
        }))

def shortlist_remove(request, candidate_id, job_id):
    ShortlistedCandidates.objects.filter(
            user_id=candidate_id,
            advertisement_id=job_id,

        ).delete()
    AdvertisementApplied.objects.filter(
            user_id=candidate_id,
            advertisement_id=job_id
        ).update(
            is_shortlisted=False
        )
    return HttpResponse(json.dumps({
        'status': True
    }))


def candidate_remove(request, candidate_id, job_id):
    AdvertisementApplied.objects.filter(
            user_id=candidate_id,
            advertisement_id=job_id
        ).update(
            candidate_status=False
        )
    return HttpResponse(json.dumps({
        'status': True
    }))


class ListShortlisted(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request, job_id):
        """
        :param request:
        :param job_id:
        :return:
        """
        data = ShortlistedCandidates.objects.raw(
            """
            SELECT *
            FROM company_shortlistedcandidates join users_userlocation on users_userlocation.user_id=company_shortlistedcandidates.user_id
            join users_userbio on users_userbio.user_id=company_shortlistedcandidates.user_id join  users_usereducation on
            users_usereducation.user_id = company_shortlistedcandidates.user_id join users_useremployment on
            users_useremployment.user_id = company_shortlistedcandidates.user_id join auth_user
            on auth_user.id = company_shortlistedcandidates.user_id join core_cities on users_userlocation.user_city_id = core_cities.id
            join core_countries on users_userlocation.user_country_id = core_countries.id left outer join
            evaluation_evaluation_result on evaluation_evaluation_result.id = company_shortlistedcandidates.user_id
            where advertisement_id={0} group by auth_user.id
            """.format(job_id)

        )
        user_employment = AdvertisementApplied.objects.raw(
            """
            SELECT * FROM company_shortlistedcandidates join users_useremployment on users_useremployment.user_id = company_shortlistedcandidates.user_id
            where advertisement_id={0}

            """.format(job_id)
        )
        user_education =  AdvertisementApplied.objects.raw("""
            SELECT * FROM company_shortlistedcandidates join users_usereducation on users_usereducation .user_id = company_shortlistedcandidates.user_id
            where advertisement_id={0}""".format(job_id)
        )
        list_total = int(len(list(data)))


        return render(request, 'shortlisted_candidates.html', {
            'data': data,
            'employment': user_employment,
            'education': user_education,
            'job_id': job_id,
            'data_count': list_total,
            'user_is_company': True,
            'body_status': is_body_status(request)
        })



class Candidate(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request, candidate_id):
        user_bio_data = users_models.UserBio.objects.filter(
            user_id=candidate_id
        )[0]
        user_location_data = users_models.UserLocation.objects.filter(
            user_id=candidate_id
        )[0]
        user_main_data = User.objects.filter(id=candidate_id)[0]
        user_education_data = users_models.UserEducation.objects.filter(user_id=candidate_id)
        user_employment_data = users_models.UserEmployment.objects.filter(user_id=candidate_id)
        user_cv_data = users_models.UserCV.objects.filter(user_id=candidate_id)[0]
        return render(request, 'candidate.html', {
            'candidate_id': candidate_id,
            'user_bio': user_bio_data,
            'user_location': user_location_data,
            'user_main': user_main_data,
            'user_education': user_education_data,
            'user_employment': user_employment_data,
            'user_cv': user_cv_data,
            'user_is_company': True,
            'body_status': is_body_status(request)
        })

class ScheduleInterview(View):
    @method_decorator(login_required)
    @method_decorator(is_company)
    def get(self, request, candidate_id, job_id):
        user_bio_data = users_models.UserBio.objects.filter(
            user_id=candidate_id
        )[0]
        user_location_data = users_models.UserLocation.objects.filter(
            user_id=candidate_id
        )[0]
        user_main_data = User.objects.filter(id=candidate_id)[0]
        user_education_data = users_models.UserEducation.objects.filter(user_id=candidate_id)
        user_employment_data = users_models.UserEmployment.objects.filter(user_id=candidate_id)
        user_cv_data = users_models.UserCV.objects.filter(user_id=candidate_id)[0]
        today_date = datetime.now()
        return render(request, 'schedule_interview_candidate.html', {
            'candidate_id': candidate_id,
            'user_bio': user_bio_data,
            'user_location': user_location_data,
            'user_main': user_main_data,
            'user_education': user_education_data,
            'user_employment': user_employment_data,
            'user_cv': user_cv_data,
            'job_id': job_id,
            'user_is_company': True,
            'body_status': is_body_status(request),
            'today_date': today_date
        })
    def post(self, request, candidate_id, job_id):

        try:
            date_str_from = request.POST['from_date'] + " " +  request.POST['from_time']
            date_str_to = request.POST['to_date'] + " " +  request.POST['to_time']
            from_full_date = datetime.strptime(date_str_from,'%Y-%m-%d %H:%M')
            to_full_date = datetime.strptime(date_str_to,'%Y-%m-%d %H:%M')
            from_time = datetime.strptime(request.POST['from_time'], '%H:%M')
            to_time = datetime.strptime(request.POST['to_time'], '%H:%M')

            get_candidate_info = User.objects.filter(id=candidate_id)[0]
            invitation_message = str(request.POST['invitation']).replace(
                '{{first_name}}', get_candidate_info.first_name
            ).replace(
                '{{from_time}}', str(from_full_date.strftime("%d %b %Y %I:%M:%S %p")),
            ).replace(
                '{{to_time}}', str(to_full_date.strftime("%d %b %Y %I:%M:%S %p")),
            )

            ShortlistedCandidates.objects.filter(
                user_id=candidate_id
            ).update(
                from_date=from_full_date,
                to_date=to_full_date,
                from_only_date=request.POST['from_date'],
                to_only_date=request.POST['to_date'],
                from_time=from_time,
                to_time=to_time,
                invitation_message=invitation_message,
                is_interview=True
            )

            # notify = str('You are invited for the interview '+ from_time +' to '+ to_time +' on '+ request.POST['from_date'] +'. Kindly be there on time.')
            # print notify

            Notification(
                title=invitation_message,
                type=0,
                status=0,
                status_read=0,
                user_id=candidate_id

            ).save()


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            if exc_tb.tb_lineno == 822 or exc_tb.tb_lineno == 823 or exc_tb.tb_lineno == 824 or exc_tb.tb_lineno == 825:
                return HttpResponse(json.dumps({'status': False, 'response':'Invalid Date Entered'}))

        #for email values

        listvalue = {
            'tosend': User.objects.filter(id=candidate_id)[0].email,
            'username': User.objects.filter(id=candidate_id)[0].username,
            'first_name': User.objects.filter(id=candidate_id)[0].first_name,
            'message': invitation_message
        }
        sendemail_ = email.EmailFunc('schedule_interview', **listvalue)
        sendemail_.generic_email()
        return HttpResponse(
            json.dumps(
                {
                    'status': True
                }
            )
        )

class SendMessage(View):
    def get(self, request):
        print 'ola'
    def post(self, request):
        Messages(
            message_title=request.POST['subject_message'],
            receiver_id=int(request.POST['candidate_id']),
            sender_id=request.user.id,
            message_body=request.POST['content_message'],
            date_send=datetime.now()
        ).save()
        return HttpResponse(
            json.dumps({
                'status': True
            })
        )

class ComposedSend(View):
    def get(self, request):
        print 'ola'
    def post(self, request):
        Messages(
            message_title=request.POST['subject_message'],
            receiver_id=int(request.POST['candidate_id']),
            sender_id=request.user.id,
            message_body=request.POST['content_message'],
            date_send=datetime.now()
        ).save()
        obj = Messages.objects.latest('id')

        html = render_to_string('company_message_send.html', {'message': obj, 'user_is_company': True})
        return HttpResponse(
            html
        )

def pdf_render(request, candidate_id):
    user_cv = users_models.UserCV.objects.filter(user_id=candidate_id)[0]
    print user_cv.user_cv_file
    if str(user_cv.user_cv_file).__contains__('.pdf'):
        with open(str(user_cv.user_cv_file), 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'filename={0}'.format(user_cv.user_cv_title)
            return response
        pdf.closed
    else:
        with open(str(user_cv.user_cv_file), 'rb') as doc_x:
            response = HttpResponse(doc_x.read(),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'filename={0}'.format(user_cv.user_cv_title)
            return response
        doc_x.closed


@login_required()
@is_company
def analytics(request, job_id):
    try:
        if AdvertisementAnalytics.objects.filter(
        advertisement_id=job_id
    )[0]:
            count_total_visitors = AdvertisementAnalytics.objects.filter(
                advertisement_id=job_id
            ).count()
            count_unique_visitors = AdvertisementAnalytics.objects.filter(
                advertisement_id=job_id
            ).values(
                'remote_address'
            ).annotate(
                total_visitors=Count(
                'remote_address',
                distinct=True

            ))
            visitors_browser = AdvertisementAnalytics.objects.values(
                'user_agent_family'
            ).annotate(total_user_agent_family=Count(
                'user_agent_family',
            )).filter(advertisement_id=job_id)
            country_visitors = AdvertisementAnalytics.objects.values(
                'country_long'
            ).filter(
                advertisement_id=job_id
            ).annotate(
                total_country_visitors=Count(
                'country_long',
            )).order_by('-total_country_visitors')[:5]
            operating_system = AdvertisementAnalytics.objects.values(
                'os_family'
            ).annotate(total_operating_system=Count(
                'os_family',
            )).filter(advertisement_id=job_id)
            gender = AdvertisementAnalytics.objects.values(
                'visitor_gender'
            ).annotate(total_visits=Count(
                'visitor_gender',
            )).filter(advertisement_id=job_id)
            print gender
            last_seven_days_date = datetime.today() - timedelta(days=7)


            print last_seven_days_date
            last_seven_days = AdvertisementAnalytics.objects.filter(post_date__gte = last_seven_days_date).values(
                'post_date'
            ).annotate(total_visitors_date=Count(
                'post_date',
            ))
            get_visitors_stats(request,job_id)

            # Gathering the Operating System information here

            linux = {}
            ubuntu = {}
            windows = {}
            mac = {}

            is_linux = next((data for data in operating_system if data['os_family'] == 'Linux'), None)
            if is_linux:
                linux['os']= is_linux['os_family']
                linux['visitors'] = is_linux['total_operating_system']
            else:
                linux['os'] = 'Linux'
                linux['visitors'] = 0
            print linux

            is_ubuntu = next((data for data in operating_system if data['os_family'] == 'Ubuntu'), None)
            if is_ubuntu:
                ubuntu['os']= is_ubuntu['os_family']
                ubuntu['visitors'] = is_ubuntu['total_operating_system']
            else:
                ubuntu['os'] = 'Ubuntu'
                ubuntu['visitors'] = 0
            print ubuntu

            is_windows = next((data for data in operating_system if data['os_family']=='Windows'), None)
            if is_windows:
                windows['os']= is_windows['os_family']
                windows['visitors'] = is_windows['total_operating_system']
            else:
                windows['os'] = 'Windows'
                windows['visitors'] = 0
            print windows
            is_mac = next((data for data in operating_system if data['os_family']=='Mac'), None)

            if is_mac:
                mac['os']= is_mac['os_family']
                mac['visitors'] = is_mac['total_operating_system']
            else:
                mac['os'] = 'Mac OS X'
                mac['visitors'] = 0

            internet_explorer, firefox, safari, chrome, opera = visitors_browsers_filter(visitors_browser) # Getting Browsers data
            male, female, unknown = gender_statistics(gender) # Getting Gender data


            print last_seven_days
            print operating_system
            print visitors_browser
            print count_unique_visitors[0]['total_visitors']
            print json.dumps([dict(item) for item in operating_system])
            count = str(last_seven_days_date)[8:10]
            _seven_days = []
            return render(
                request,
                'analytics_jobad.html',
                {
                    'seven_days_date': str(last_seven_days_date)[8:10],
                    'seven_days': [dict(item) for item in last_seven_days],
                    'visitors_data': get_visitors_stats(request, job_id),
                    'country_visitors': [dict(item) for item in country_visitors],
                    'visitors_browser': [dict(item) for item in visitors_browser],
                    'operating_system': [dict(item) for item in operating_system],
                    'total_unique_visitors': count_unique_visitors[0]['total_visitors'],
                    'total_visitors': count_total_visitors,
                    'linux': linux,
                    'windows': windows,
                    'mac': mac,
                    'ubuntu': ubuntu,
                    'opera': opera,
                    'internet_explorer': internet_explorer,
                    'firefox': firefox,
                    'safari': safari,
                    'chrome': chrome,
                    'male': male,
                    'female':female,
                    'unknown': unknown,
                    'user_is_company': True,
                    'body_status': is_body_status(request)
                }
            )
    except:
        return render(
            request,
            'no_analytics.html',
            {
               'user_is_company': True
            }
        )


def get_visitors_stats(request, job_id):
    """ Getting visitors stats on daily basis """
    data = {}
    seventh_day = datetime.today() - timedelta(days=7)
    sixth_day = datetime.today() - timedelta(days=6)
    fifth_day = datetime.today() - timedelta(days=5)
    fourth_day = datetime.today() - timedelta(days=4)
    third_day = datetime.today() - timedelta(days=3)
    second_day = datetime.today() - timedelta(days=2)
    first_day = datetime.today() - timedelta(days=1)
    today_day = datetime.today()

    #seven day data
    seventh = get_date_data(request, job_id, seventh_day)

    #sixth day data
    sixth = get_date_data(request, job_id, sixth_day)

    #fifth day data
    fifth = get_date_data(request, job_id, fifth_day)

    #fourth day data
    fourth = get_date_data(request, job_id, fourth_day)

    #third day data
    third = get_date_data(request, job_id, third_day)

    #second day data
    second = get_date_data(request, job_id, second_day)

    #first day data
    first = get_date_data(request, job_id, first_day)
    #first day data
    today = get_date_data(request, job_id, today_day)

    # Getting the visitors data based on the date
    # Creating the dict to return the data

    visitors_data = {
        'seventh': get_visitors(seventh_day, seventh),
        'sixth': get_visitors(sixth_day, sixth),
        'fifth': get_visitors(fifth_day, fifth),
        'fourth': get_visitors(fourth_day, fourth),
        'third': get_visitors(third_day, third),
        'second': get_visitors(second_day, second),
        'first': get_visitors(first_day, first),
        'today': get_visitors(today_day, today)

    }
    return visitors_data


def get_date_data(request, job_id, day):
    """Filtering the object based on the date and job id"""
    data = AdvertisementAnalytics.objects.filter(
        post_date = day,
        advertisement_id=job_id
    ).values(
        'post_date'
    ).annotate(total_visitors_date=Count(
        'post_date',
    ))
    return data

def get_visitors(date_value, object):
    """Checking Each object date and counting total visitors"""
    data = {}
    try:
        if object:
            data['date'] = date_value
            data['visitors'] = object[0]['total_visitors_date']

        else:
            data['date'] = date_value
            data['visitors'] = 0
    except Exception as e:
        print e
        data['date'] = date_value
        data['visitors'] = 0
        pass
    return data


def visitors_browsers_filter(browsers):
    """Filtering Browsers Data"""
    internet_explorer = {}
    firefox = {}
    safari = {}
    chrome = {}
    opera = {}
    is_ie = next((data for data in browsers if data['user_agent_family'] == 'Internet Explorer'), None)
    if is_ie:
        internet_explorer['user_agent']= is_ie['user_agent_family']
        internet_explorer['visitors'] = is_ie['total_user_agent_family']
    else:
        internet_explorer['user_agent'] = 'Internet Explorer'
        internet_explorer['visitors'] = 0
    is_firefox = next((data for data in browsers if data['user_agent_family'] == 'Firefox'), None)
    if is_firefox :
        firefox['user_agent']= is_firefox['user_agent_family']
        firefox['visitors'] = is_firefox['total_user_agent_family']
    else:
        firefox['user_agent'] = 'Firefox'
        firefox['visitors'] = 0
    is_safari = next((data for data in browsers if data['user_agent_family']=='Safari'), None)
    if is_safari:
        safari['user_agent']= is_safari['user_agent_family']
        safari['visitors'] = is_safari['total_user_agent_family']
    else:
        safari['user_agent'] = 'Safari'
        safari['visitors'] = 0
    is_chrome= next((data for data in browsers if data['user_agent_family']=='Chrome'), None)
    if is_chrome:
        chrome['user_agent']= is_chrome['user_agent_family']
        chrome['visitors'] = is_chrome['total_user_agent_family']
    else:
        chrome['user_agent'] = 'Chrome'
        chrome['visitors'] = 0
    is_opera = next((data for data in browsers if data['user_agent_family']=='Opera'), None)
    if is_opera:
        opera['user_agent']= is_opera['user_agent_family']
        opera['visitors'] = is_opera['total_user_agent_family']
    else:
        opera['user_agent'] = 'Chrome'
        opera['visitors'] = 0
    return internet_explorer, firefox, safari, chrome, opera


def gender_statistics(gender):
    """Filtering Gender Statistics"""
    male = {}
    female = {}
    unknown = {}
    is_male = next((data for data in gender if data['visitor_gender']==0), None)
    if is_male:
        male['visitors'] = is_male['total_visits']
    else:
        male['visitors'] = 0
    is_female = next((data for data in gender if data['visitor_gender']==1), None)
    if is_female:
        female['visitors'] = is_female['total_visits']
    else:
        female['visitors'] = 0
    is_unknown = next((data for data in gender if data['visitor_gender']==2), None)
    if is_unknown:
        unknown['visitors'] = is_unknown['total_visits']
    else:
        unknown['visitors'] = 0
    return male, female, unknown


class CompanyAppliedAll(View):
    def get(self, request):
        group_jobs = AdvertisementApplied.objects.raw(
            """SELECT count(*) as applied_job_user, company_advertisement.id , company_advertisement.job_title
            FROM company_advertisementapplied join users_userlocation on
            users_userlocation.user_id=company_advertisementapplied.user_id join users_userbio on
            users_userbio.user_id=company_advertisementapplied.user_id join users_usereducation on
            users_usereducation.user_id = company_advertisementapplied.user_id join users_useremployment on
            users_useremployment.user_id = company_advertisementapplied.user_id join auth_user on
            auth_user.id = company_advertisementapplied.user_id join core_cities on
            users_userlocation.user_city_id = core_cities.id join core_countries on
            users_userlocation.user_country_id = core_countries.id left outer join
            evaluation_evaluation_result on evaluation_evaluation_result.user_id =
            company_advertisementapplied.user_id join company_advertisement on
            company_advertisement.id = company_advertisementapplied.advertisement_id where
            company_user_id = {0} and company_advertisementapplied.candidate_status=TRUE
            group by company_advertisement.id
            """.format(request.user.id))

        data = AdvertisementApplied.objects.raw(
            """
            SELECT * FROM company_advertisementapplied join users_userlocation on
            users_userlocation.user_id=company_advertisementapplied.user_id join users_userbio on
            users_userbio.user_id=company_advertisementapplied.user_id join users_usereducation on
            users_usereducation.user_id = company_advertisementapplied.user_id join users_useremployment on
            users_useremployment.user_id = company_advertisementapplied.user_id join auth_user on
            auth_user.id = company_advertisementapplied.user_id join core_cities on
            users_userlocation.user_city_id = core_cities.id join core_countries on
            users_userlocation.user_country_id = core_countries.id left outer join
            evaluation_evaluation_result on evaluation_evaluation_result.user_id =
            company_advertisementapplied.user_id join company_advertisement on company_advertisement.id =
            company_advertisementapplied.advertisement_id where company_advertisement.id = {0}
            and company_advertisementapplied.candidate_status=TRUE group by auth_user.id
            """.format(group_jobs[0].id))


        user_employment = AdvertisementApplied.objects.raw(
            """
            SELECT * FROM company_advertisementapplied join users_useremployment on users_useremployment.user_id = company_advertisementapplied.user_id
            where advertisement_id = {0} and company_advertisementapplied.candidate_status=TRUE group by advertisement_id
            """.format(group_jobs[0].id))
        user_education =  AdvertisementApplied.objects.raw("""
            SELECT * FROM company_advertisementapplied join users_usereducation on users_usereducation .user_id = company_advertisementapplied.user_id
            where advertisement_id = {0} and company_advertisementapplied.candidate_status=TRUE group by advertisement_id
            """.format(group_jobs[0].id)
        )

        is_evaluation_test = Advertisement.admanager.all()[0].is_evaluation_test
        list_total = int(len(list(data)))
        return render(request, 'applied_candidates_all.html', {
            'data': data,
            'group_jobs': group_jobs,
            'employment': user_employment,
            'education': user_education,
            'data_count': list_total,
            'user_is_company': True,
            'is_evaluation_test': is_evaluation_test,
            'body_status': is_body_status(request)
        })

    def post(self, request):
        print request.POST

        data = AdvertisementApplied.objects.raw(
            """
            SELECT * FROM company_advertisementapplied join users_userlocation on
            users_userlocation.user_id=company_advertisementapplied.user_id join users_userbio on
            users_userbio.user_id=company_advertisementapplied.user_id join users_usereducation on
            users_usereducation.user_id = company_advertisementapplied.user_id join users_useremployment on
            users_useremployment.user_id = company_advertisementapplied.user_id join auth_user on
            auth_user.id = company_advertisementapplied.user_id join core_cities on
            users_userlocation.user_city_id = core_cities.id join core_countries on
            users_userlocation.user_country_id = core_countries.id left outer join
            evaluation_evaluation_result on evaluation_evaluation_result.user_id =
            company_advertisementapplied.user_id join company_advertisement on company_advertisement.id =
            company_advertisementapplied.advertisement_id where company_advertisement.id = {0} and
            company_advertisementapplied.candidate_status=TRUE
            group by auth_user.id
            """.format(request.POST['job_id']))

        user_employment = AdvertisementApplied.objects.raw(
            """
            SELECT * FROM company_advertisementapplied join users_useremployment on users_useremployment.user_id =
             company_advertisementapplied.user_id where advertisement_id = {0} and
             company_advertisementapplied.candidate_status=TRUE group by advertisement_id
            """.format(request.POST['job_id']))
        user_education =  AdvertisementApplied.objects.raw("""
            SELECT * FROM company_advertisementapplied join users_usereducation on users_usereducation .user_id =
            company_advertisementapplied.user_id where advertisement_id = {0} and
            company_advertisementapplied.candidate_status=TRUE group by advertisement_id
            """.format(request.POST['job_id']))
        html = render_to_string('applied_candidate_dynamic_all.html', {'data': data,'employment': user_employment,
                                                                   'education': user_education
                                                                   }, context_instance=RequestContext(request))
        return HttpResponse(html)


class CompanyShortlistedAll(View):

    def get(self, request):
        """

        :param request:
        :return:
        """

    def post(self, request):
        """

        :param request:
        :return:
        """


class Message_nofication(View):
    def get(self,request):
        # message_count = Messages.objects.raw(
        #     """
        #      SELECT * from company_messages join auth_user ON auth_user.id = company_messages.receiver_id
        #      where receiver_id={0} and status_read=0
        #      group by auth_user.id order by company_messages.date_send
        #     """.format(request.user.id)
        # )

        message_count = Messages.objects.filter(receiver_id=request.user.id,status_read=0).count()
        print message_count


        return HttpResponse(json.dumps({'number_messages':int(message_count)}))



    def post(self,request):
        try:

            query = Messages.objects.filter(receiver_id=request.user.id,status_read=0).update(status_read=1)

            if query:
                  return HttpResponse(json.dumps({'status':'True'}))
        except Exception as e:
           print e

class Admin_notify(View):
    def get(self,request):
        query = Notification.objects.filter(user_id=request.user.id,status_read=0).count()
        return HttpResponse(json.dumps({'notify':int(query)}))

    def post(self,request):
        return HttpResponse(json.dumps({'number_messages':'True'}))

class Get_notify(View):
    def get(self,request):
        query = Notification.objects.filter(user_id=request.user.id).order_by('-id')[:5]
        query2=Notification.objects.filter(user_id=request.user.id,status_read=0).update(status_read=1)


        wholedata = serializers.serialize('json', query)        # query2 = serializers(query)
        return HttpResponse(json.dumps({'status':wholedata}))



class View_all_notification(View):

    def get(self,request):
        try:
           query = Notification.objects.filter(user_id=request.user.id).order_by('-id')
           page = request.GET.get('page')
           query2 = pagination_page(page,query)
           if query and query2:
               return render(request,'company_notification.html',{'data':query2,'user_is_company': True})
           else :
               return render(request,'company_notification.html',{'user_is_company': True})
        except Exception as e:
           return render(request,'company_notification.html',{'user_is_company': True})

class Delete_notification(View):

    def post(self,request):
        try:
           query = Notification.objects.filter(id=int(request.POST['id'])).delete()

           if not query:
                return HttpResponse(json.dumps({'status':True}))
           else:
               return HttpResponse(json.dumps({'status':False}))
        except Exception as e:
           print e

class JobSeeker_View_all_notification(View):
    def get(self,request):
        try:
           query = Notification.objects.filter(user_id=request.user.id).order_by('-id')
           page = request.GET.get('page')
           query2 = pagination_page(page,query)
           if query and query2:
               return render(request,'jobseeker_notification.html',{'data':query2})
           else :
               return render(request,'jobseeker_notification.html')
        except Exception as e:
           return render(request,'jobseeker_notification.html')


class Jobseeker_Delete_notification(View):
     def post(self,request):
        try:
           query = Notification.objects.filter(id=int(request.POST['id'])).delete()

           if not query:
                return HttpResponse(json.dumps({'status':True}))
           else:
               return HttpResponse(json.dumps({'status':False}))
        except Exception as e:
           print e


def pagination_page(page,data):
        paginator = Paginator(data, 8) # Show 25 contacts per page

        try:
           data = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
           data = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            data = paginator.page(paginator.num_pages)
        return data