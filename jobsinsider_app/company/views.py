from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login as login_session
from django.utils import timezone
from django.db.models import Count
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from accounts import models as acc_mod
from core.decoraters import is_company
from accounts import forms as accountsform
from datetime import datetime, timedelta
from urlparse import urlparse, parse_qs
from user_agents import parse
from forms import *
import simplejson as json


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
        return render(request, 'company_dashboard.html', {
            'body_status': status,
            'profile_form': company_profile,
            'posted_jobs': posted_jobs,
            'job_details': jobs_details,
            'total_applications': total_applications
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
        status  = is_body_status(request)
        return render(
            request,
            'job_advertisement.html',
            {
                'job_form': jobad,
                'body_status': status
            }
        )

    def post(self, request):
        parameters = parse_qs(request.POST['form_val'])
        resp = {}
        try:
            get_company_name = CompanyProfile.objects.filter(
                user_id=request.user.id
            )[0].company_name
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
                company_user_id=request.user.id,
                company = get_company_name
            ).save()

            resp['status']= True    # when the query succeed.
            resp['last_inserted'] = Advertisement.admanager.latest('id').id

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
        status = is_body_status(request)
        return render(request, 'job_advertisement_edit.html', {
            'job_form': jobad,
            'jobid': job_id,
            'job_approval_status': data[0].job_approval_status,
            'body_status': status
        })
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
                'body_status': status
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
                'body_status': is_body_status(request)
             }
        )
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
                'body_status': is_body_status(request)
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
            join core_countries on users_userlocation.user_country_id = core_countries.id where advertisement_id={0}
            group by auth_user.id
            """.format(job_id)

        )
        user_employment = AdvertisementApplied.objects.raw(
            """
            SELECT * FROM company_advertisementapplied join users_useremployment on users_useremployment.user_id = company_advertisementapplied.user_id
            where advertisement_id={0}

            """.format(job_id)
        )
        user_education =  AdvertisementApplied.objects.raw("""
            SELECT * FROM company_advertisementapplied join users_usereducation on users_usereducation .user_id = company_advertisementapplied.user_id
            where advertisement_id={0}""".format(job_id)
        )
        list_total = int(len(list(data)))
        return render(request, 'applied_candidates.html', {
            'data': data,
            'employment': user_employment,
            'education': user_education,
            'job_id': job_id,
            'data_count': list_total
        })


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
            join core_countries on users_userlocation.user_country_id = core_countries.id where advertisement_id={0}
            group by auth_user.id
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
            'data_count': list_total
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
            'user_cv': user_cv_data
        })

class ScheduleInterview(View):
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
        return render(request, 'schedule_interview.html', {
            'candidate_id': candidate_id,
            'user_bio': user_bio_data,
            'user_location': user_location_data,
            'user_main': user_main_data,
            'user_education': user_education_data,
            'user_employment': user_employment_data,
            'user_cv': user_cv_data
        })

def pdf_render(request, candidate_id):
    user_cv = users_models.UserCV.objects.filter(user_id=candidate_id)[0]
    print user_cv.user_cv_file
    if str(user_cv.user_cv_file).__contains__('.pdf'):
        with open(str(user_cv.user_cv_file), 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'filename=crowfoot_ERD_name.pdf'
            return response
        pdf.closed
    else:
        with open(str(user_cv.user_cv_file), 'rb') as doc_x:
            response = HttpResponse(doc_x.read(),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'filename=crowfoot_ERD_name.doc'
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
                    'unknown': unknown
                }
            )
    except:
        return render(
            request,
            'no_analytics.html'
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
