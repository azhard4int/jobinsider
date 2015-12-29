import simplejson as json

from django.shortcuts import render
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core import serializers
from django import views
from models import *
from forms import *
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import  method_decorator
from django.contrib.auth import login as login_session
from django.core import serializers
from django.core.exceptions import MultipleObjectsReturned

import logging
import os

from accounts import models as accountsmodels
from accounts import forms as accountsform
from company import models as company_models
from core.decoraters import *
from core import models as core_models
from core import email
from datetime import datetime
from itertools import chain


# Create your views here.
@login_required
def index(request):
    """
    Whole view for the company - starting out from the selection of the website.
    """
    step_value = request.GET.get('step', '')
    list_categories = UserSkills()
    if request.user.is_active:
        """
        Adding the check if its company user then show different dashboard
        """
        if UserSkills.objects.exist_not(request.user.id):
            HttpResponseRedirect('/user')   # later on have to change the request
        if is_company_true(request.user.id):
            return HttpResponseRedirect('/company/index')
        user_profile = UserBioInfo()
        user_location = UserLocationForm()
        detect_user = UserBio.objects.filter(user_id=request.user.id)
        if detect_user:
            return HttpResponseRedirect('/user/profile_cv')
        return render(
            request, 'user_biography.html',
            {
                'userbio': user_profile,
                'userloc': user_location
            }
        )

        # if step_value == '4':
        #     user_cv_data = cv_object_ret(request.user.id)
        #     if user_cv_data.user_cv_builder == 0:
        #         return HttpResponseRedirect('/user/dashboard/')
        #     elif user_cv_data.user_cv_builder==1:
        #         """
        #         CV builder further detials include
        #         user_graduation status along with other info.
        #         """
        #         return HttpResponseRedirect('/user/education/')
    else:
        HttpResponseRedirect('/accounts/signup/confirm-email')


class UserDashboard(View):

    @method_decorator(login_required)
    def get(self, request):
        jobs_details = company_models.Advertisement.admanager.filter(
            job_approval_status=1
        ).order_by('-submission_date')[:5]
        applied_jobs = company_models.AdvertisementApplied.objects.filter(
            user_id=request.user.id
        ).count()
        # shortlisted_jobs =
        favorite_jobs = company_models.AdvertisementFavorite.objects.filter(
            user_id=request.user.id
        ).count()
        interviews_total_scheduled = company_models.ShortlistedCandidates.objects.filter(user_id=request.user.id,
                                                                                         is_interview=True).count()
        total_shortlisted = company_models.ShortlistedCandidates.objects.filter(user_id=request.user.id).count()
        get_categories = core_models.Categories.objects.get_all()
        return render(
            request,
            'profile_dashboard.html',
            {
                'job_detail': jobs_details,
                'applied_jobs': applied_jobs,
                'favorite_jobs': favorite_jobs,
                'categories': get_categories,
                'total_interviews': interviews_total_scheduled,
                'total_shortlisted': total_shortlisted,
                'body_status': 0
            }
        )

# @login_required()

def cv_object_ret(user_id):
    try:
        user_cv_data = UserCV.objects.filter(user_id=user_id)[0]
    except IndexError:
        user_cv_data = False
    return user_cv_data

@login_required()
def skills_list(request):
    """
    This function is to retrieve the skills list based on event triggered
    from user side.
    """
    if request.method == 'POST':
        skill = UserSkills()
        skill_data = skill.get_skills(request.POST['cat_id'])
        # data_id =
        # if skill_data:
        #     skill_data.id
        json_data = serializers.serialize('json', skill_data)
        return HttpResponse(json_data)
    else:
        HttpResponseRedirect('/user/')


@login_required()
def skills(request):
    """
    Storing newly registered details and storing them into the database.
    """

    if request.method == 'POST':
        category_id = request.POST['category_id']
        skills = request.POST['skills_value']
        user = request.user
        userobj = UserSkills(
            user_id=user.id,
            skills=skills,
            category_id=category_id,
            skill_status=1
        )
        try:
            save_data = userobj.save()
            if save_data:
                return HttpResponse(json.dumps({'status': False}))
            else:
                return HttpResponse(json.dumps({'status': True}))
        except:
            return HttpResponse(json.dumps({'status': False}))


@login_required()
def cities(request):
    """
    Fetch cities based on the ID
    """
    if request.method == 'POST':
        list = core_models.Cities.objects.filter(country_id=request.POST['country_id']).all().order_by('city_name')
        cities = [ab.city_name for ab in list]
        cities_list = serializers.serialize('json', list)
        # for ab in list:
        #     ab.city_name
        return HttpResponse(json.dumps({'cities': cities_list}))
    else:
        raise Http404


class UserInfo(View):
    """
    This section includes the user biography and CV builder.
    """
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Handling the user basic profile information
        """
        detect_user = UserBio.objects.filter(user_id=request.user.id)
        if detect_user:
            return HttpResponse(json.dumps({'status': True}))
        if request.method == 'POST':
            form = UserBioInfo(request.POST, request.FILES)
            print User.objects.filter(id=request.user.id)
            print request.POST
            if form.is_valid():

                print User.objects.filter(id=request.user.id)
                # UserBio(commit=False)
                try:
                    print request.FILES
                    print request.POST['user_title'],
                    print request.FILES['user_portrait'].name
                    print User.objects.filter(id=request.user.id)[0]
                    user_bio=UserBio(
                        user=User.objects.filter(id=request.user.id)[0],
                        user_bio_status=1,
                        user_portrait=request.FILES['user_portrait'],
                        user_title=request.POST['user_title'],
                        user_overview=request.POST['user_overview'],
                        user_language_pre=request.POST['user_language_pre'],
                        user_gender=request.POST['user_gender'],
                        user_portrait_filename = str(request.FILES['user_portrait'].name),
                    ).save()
                    # user_bio.
                    # storing user location details
                    user_location = UserLocation(
                        user_address = request.POST['user_address'],
                        user_city_id = request.POST['user_city'],
                        user_country_id = request.POST['user_country'],
                        user_zipcode = request.POST['user_zipcode'],
                        user_phone_no = request.POST['user_phone_no'],
                        user_location_status = 1,
                        user = User.objects.filter(id=request.user.id)[0]

                    )
                    user_location.save()
                except IntegrityError:
                    # print e
                    return HttpResponse(json.dumps({'status': True}))
                return HttpResponse(json.dumps({'status': True}))


class UserCVUpload(View):
    """
    Uploading user cv through it
    """
    @method_decorator(login_required)

    def get(self, request, *args, **kwargs):
        """
        """
        user_status = accountsmodels.UserProfile.objects.filter(
                user_id=request.user.id
        )[0]
        user_cv_data = cv_object_ret(request.user.id)
        if user_cv_data:    # user CV table status should be 0 and user profile status should be 0
            if user_cv_data.user_cv_builder == 0 or user_status.user_cv_status == 1:
                return HttpResponseRedirect('/user/add_employment/')
        cvform = UserCVForm()
        return render(request, 'cv_selection_page.html', {'user_cv_form': cvform,'body_status': 0})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Detect the user CV Post Data and upload it out!
        Accepted formats are .pdf, .docx, .doc
        """
        if request.method == 'POST':
            cvform = UserCVForm(request.POST, request.FILES)
            if cvform.is_valid():
                userCVobj = UserCV()
                userCVobj.user_cv_title = request.FILES['user_cv_file'].name
                userCVobj.user_cv_file = request.FILES['user_cv_file']
                userCVobj.user = User.objects.filter(id=request.user.id)[0]
                userCVobj.save()
                accountsmodels.UserProfile.objects.filter(user_id=request.user.id).update(user_cv_status=1)
                return HttpResponse(json.dumps({'status': True}))


@login_required()
def is_cv_builder(request):
    if request.method == 'POST':
        UserCV(
            user_cv_title= 0,
            user_cv_file= 0,
            user_id=request.user.id,
            user_cv_builder_status=1,
            user_cv_builder=1
        ).save()

        accountsmodels.UserProfile.objects.filter(user_id=request.user.id).update(user_cv_status=1)
        return HttpResponse(json.dumps({'status': True}))


def AddCVEmployment(request):
    """
    No need in the future , used clone function instead of it.
    """
    if request.method == 'POST':
        # data = serializers.serialize('json', cvform)
        cvemploy = AddUserEmploymentForm()
        # data = {
        #     # 'company_location': cvemploy.company_location,
        #     'company_name': cvemploy.company_name,
        #     'company_worktitle': cvemploy.company_worktitle,
        #     'company_from': cvemploy.company_from,
        #     'company_to': cvemploy.company_to,
        #     'company_role': cvemploy.company_role,
        # }
        # print data
        return HttpResponse((cvemploy))


class AddUserEmployment(View):
    """
     User Work history page//cv builder.
    """
    @method_decorator(login_required)
    def get(self, request):

        user_cv = UserCV.objects.filter(user_id=request.user.id)[0]
        is_exist = False
        is_exist_education = False
        if UserEmployment.objects.filter(user_id=request.user.id).count() >0:
            is_exist= True
        if UserEducation.objects.filter(user_id=request.user.id).count() >0:
            is_exist_education= True
        employment_history = UserEmployment.objects.filter(user_id=request.user.id)
        education_history = UserEducation.objects.filter(user_id=request.user.id)
        if user_cv.user_cv_emp_status == 0:
            cvemploy = InitialEmploymentForm()
            eduform = EducationForm()
            return render(
                request,
                'user_employment.html',
                {
                    'cv_employ': cvemploy,
                    'is_exist': is_exist,
                    'is_exist_education': is_exist_education,
                    'employment_user': employment_history,
                    'education_user': education_history,
                    'edu': eduform,
                    'body_status': 0
                }
            )
        if user_cv.user_cv_emp_status == 1: #and user_cv.user_cv_builder==0
                return HttpResponseRedirect('/user/dashboard/')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            c_worktitle = request.POST.getlist('company_worktitle')[0]
            c_name = request.POST.getlist('company_name')[0]
            c_location = request.POST.getlist('company_location')[0]
            c_role = request.POST.getlist('company_role')[0]
            c_from = request.POST.getlist('company_from')[0]
            c_to = request.POST.getlist('company_to')[0]
            # c_description = request.POST.getlist('company_description')[ab]
            user = UserEmployment(
                user_id=request.user.id,
                company_name=c_name,
                company_location=c_location,
                company_worktitle=c_worktitle,
                company_role=c_role,
                company_from =c_from,
                company_to =c_to,
                    # company_description =,
                ).save()

            user_data = UserEmployment.objects.latest('id')
            data = render_to_string(
                'employment.html',
                {
                    'user': user_data
                }
            )
            return HttpResponse(data)
                # UserCV.objects.filter(user_id=request.user.id).update(
                #     user_cv_emp_status=1
                # )

        except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': False}))

        return HttpResponse(json.dumps({'status': True}))


class EducationUpdate(View):
    """
    User Profile Education/Typically for CV builders
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        _c = UserCV.objects.filter(user_id=request.user.id)[0]
        print _c
        if _c:
            if _c.user_cv_education==1:
                return HttpResponseRedirect('/user/dashboard')
            else:
                EduForm = EducationForm()
                return render(request, 'profile_education.html', {'edu': EduForm})
                # self.show_form(request)
        else:
            # self.show_form(request)
            EduForm = EducationForm()
            return render(request, 'profile_education.html', {'edu': EduForm})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                user_institute = request.POST.getlist('user_institute')[0]
                user_degree = request.POST.getlist('user_degree')[0]
                degree_from = request.POST.getlist('degree_from')[0]
                degree_to = request.POST.getlist('degree_to')[0]
                # c_description = request.POST.getlist('company_description')[ab]
                user = UserEducation(
                    user_id=request.user.id,
                    user_institute=user_institute,
                    user_degree=user_degree,
                    degree_from=degree_from,
                    degree_to=degree_to,
                    # company_description =,
                ).save()

                    # UserCV.objects.filter(user_id=request.user.id).update(
                    #     user_cv_education=1
                    # )
                user_data = UserEducation.objects.latest('id')
                data = render_to_string(
                    'education.html',
                    {
                        'user': user_data
                    }
                )
                return HttpResponse(data)
            except Exception as e:
                print e

    def show_form(self, request):
        EduForm = EducationForm()
        return render(request, 'profile_education.html', {'edu': EduForm})


@login_required()
def remove_employment(request, emp_id):
    UserEmployment.objects.filter(
        id=emp_id,
        user_id=request.user.id
    ).delete()
    return HttpResponse(json.dumps({
        'status': True
    }))


@login_required()
def remove_education(request, edu_id):
    UserEducation.objects.filter(
        id=edu_id,
        user_id=request.user.id
    ).delete()
    return HttpResponse(json.dumps({
        'status': True
    }))


@login_required()
def complete_profile(request):
     UserCV.objects.filter(user_id=request.user.id).update(
         user_cv_education=1,
         user_cv_emp_status=1
     )
     return HttpResponse(json.dumps({
        'status': True
    }))


class UserBioUpdate(View):

    def get(self, request, *args, **kwargs):
        """
        """

    def post(self, request, *args, **kwargs):
        """
        """

class Profile(View):
    """
    Update user profile view
    """
    @method_decorator(login_required)
    @method_decorator(is_job_seeker)
    def get(self, request, username=None):

        user_basic = accountsform.UserForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username,

        })
        return render(request, 'user_profile.html', {'user_basic_form': user_basic,'body_status': 0})

    @method_decorator(login_required)
    def post(self, request):
          if request.method=='POST':
              """
              check email is changed or not.
              """
              email = User.objects.filter(email=request.POST['email'])
              if email:

                  update = User.objects.filter(id=request.user.id).update(
                      first_name=request.POST['first_name'],
                      last_name=request.POST['last_name'],
                  )
                  return HttpResponse(json.dumps({'status':True}))
              else:
                  """
                  Send confirmation email first.:to do
                  """
                  update = User.objects.filter(id=request.user.id).update(
                      first_name=request.POST['first_name'],
                      last_name=request.POST['last_name'],
                      email = request.POST['email'],
                  )
                  return HttpResponse(json.dumps({'status':True}))


class ProfileChangePassword(View):

    @method_decorator(login_required)
    @method_decorator(is_job_seeker)
    def get(self, request):
        change_password = accountsform.ChangeProfilePassword()
        return render(request, 'user_change_password.html', {'cp': change_password, 'body_status': 0})

    @method_decorator(login_required)
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


class ProfileUser(View):
    @method_decorator(login_required)
    @method_decorator(is_job_seeker)
    def get(self, request):
        data = User.objects.prefetch_related('userbio','usercv','userskills', 'userlocation').get(id=request.user.id)
        employment_data =UserEmployment.objects.filter(user_id=request.user.id)
        portrait = str(data.userbio.user_portrait)
        portrait = portrait[portrait.find('/media'):]
        #country = core_models.Countries.objects.filter(id=data.userlocation.user_country)[0]
        #city = core_models.Cities.objects.filter(id=data.userlocation.user_city)[0]
        education = UserEducation.objects.filter(user_id=request.user.id)

        main = {
            'first_name': data.first_name,
            'last_name': data.last_name,
            'overview': data.userbio.user_overview,
            'email': data.email,
            'contact': data.userlocation.user_phone_no,
            'address': data.userlocation.user_address,
            'portrait': portrait,
            'country': data.userlocation.user_country,
            'city': data.userlocation.user_city
        }
        print main
        return render(request, 'profile.html', {
            'user_profile': main,
            'user_employment': employment_data,
            'user_education': education,
            'body_status': 0
        })


class ProfileSettings(View):
    """
    To update the basic profile details of a user over here.
    """
    @method_decorator(login_required)
    @method_decorator(is_job_seeker)
    def get(self, request):
        data = User.objects.prefetch_related('userbio','usercv','userskills', 'userlocation').get(id=request.user.id)
        employment_data =UserEmployment.objects.filter(user_id=request.user.id)
        portrait = str(data.userbio.user_portrait)
        portrait = portrait[portrait.find('/media'):]
        # country = core_models.Countries.objects.filter(id=data.userlocation.user_country)[0]
        # city = core_models.Cities.objects.filter(id=data.userlocation.user_city)[0]
        education = UserEducation.objects.filter(user_id=request.user.id)


        main={
            'first_name': data.first_name,
            'last_name': data.last_name,
            'overview': data.userbio.user_overview,
            'email': data.email,
            'contact': data.userlocation.user_phone_no,
            'address': data.userlocation.user_address,
            'portrait': portrait,
            'country': data.userlocation.user_country,
            'city': data.userlocation.user_city,
        }
        print data.userlocation.user_city_id
        locationForm = ProfileSettingsForm(initial={
            'user_city':data.userlocation.user_city_id,
            'user_country':data.userlocation.user_country_id,

        })
        userBioForm = UserBioInfo()

        return render(request, 'profile_settings.html', {
            'user': main,
            'user_employment': employment_data,
            'user_education': education,
            'locationForm': locationForm,
            'userBio': userBioForm,
            'user_cv_status': data.usercv.user_cv_builder_status,
            'body_status': 0
        })

    def post(self, request):
        if request.POST and request.FILES:
            self.update_biography(request)
            directory_path = str(settings.MEDIA_ROOT + "/userprofile/")
            user_value = UserBio.objects.filter(
                user_id=request.user.id
            )[0]
            user_value.user_portrait=request.FILES['user_portrait']
            user_value.user_portrait_filename = str(request.FILES['user_portrait'].name)
            user_value.save()
            return HttpResponse(json.dumps({'status':True}))

        elif request.POST:
            self.update_biography(request)
            return HttpResponse(json.dumps({'status':True}))

    def update_biography(self, request):
        """
        Updating the user bio details except for the image.
        :param request:
        :return:
        """
        user_update = User.objects.filter(id=request.user.id).update(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
        )
        location_update = UserLocation.objects.filter(
                user_id=request.user.id
        ).update(
            user_country=request.POST['user_country'],
            user_city=request.POST['user_city']
        )
        userbio_update = UserBio.objects.filter(
            user_id=request.user.id
        ).update(
            user_overview=request.POST['user_profile_overview']
        )


class ProfileSettingsEducation(View):
    @method_decorator(login_required)
    @method_decorator(is_job_seeker)
    def get(self, request):
        data = User.objects.prefetch_related('userbio','usercv','userskills', 'userlocation').get(id=request.user.id)
        employment_data =UserEmployment.objects.filter(user_id=request.user.id)
        portrait = str(data.userbio.user_portrait)
        portrait = portrait[portrait.find('/media'):]
        # country = core_models.Countries.objects.filter(id=data.userlocation.user_country)[0]
        # city = core_models.Cities.objects.filter(id=data.userlocation.user_city)[0]
        education = UserEducation.objects.filter(user_id=request.user.id)
        main = {
            'first_name': data.first_name,
            'last_name': data.last_name,
            'overview': data.userbio.user_overview,
            'email': data.email,
            'contact': data.userlocation.user_phone_no,
            'address': data.userlocation.user_address,
            'portrait': portrait,
            'country': data.userlocation.user_country,
            'city': data.userlocation.user_city,
        }
        eduform = EducationForm()
        return render(request, 'profile_settings_education.html', {
            'user': main,
            'user_employment': employment_data,
            'user_education': education,
            'edu': eduform,
            'user_cv_status': data.usercv.user_cv_builder_status,
            'body_status': 0

        })

    def post(self, request):
        data = UserEducation.objects.filter(user_id=request.user.id, id=request.POST['education_id'])[0]
        education_data = {
            'user_institute': data.user_institute,
            'user_degree': data.user_degree,
            'degree_from': str(data.degree_from),
            'degree_to': str(data.degree_to),
            # 'company_description': data.company_description,
        }
        return HttpResponse(json.dumps({'data': education_data}))


def edit_education_description(request):
    data = UserEducation.objects.filter(id=request.POST['education_id']).update(
        user_institute=request.POST['user_institute'],
        user_degree=request.POST['user_degree'],
        degree_from=request.POST['degree_from'],
        degree_to=request.POST['degree_to']
    )
    return HttpResponse(json.dumps({'status':True}))


def delete_education_description(request):
    data = UserEducation.objects.filter(user_id=request.user.id, id=request.POST['education_id']).delete()
    return HttpResponse(json.dumps({'status':True}))


class ProfileSettingsEmployment(View):
    @method_decorator(login_required)
    @method_decorator(is_job_seeker)
    def get(self, request):
        data = User.objects.prefetch_related('userbio','usercv','userskills', 'userlocation').get(id=request.user.id)
        employment_data =UserEmployment.objects.filter(user_id=request.user.id)
        portrait = str(data.userbio.user_portrait)
        portrait = portrait[portrait.find('/media'):]
        education = UserEducation.objects.filter(user_id=request.user.id)
        cvemploy = InitialEmploymentForm()
        return render(request, 'profile_settings_employment.html', {
            'user_employment': employment_data,
            'user_education': education,
            'cv_employ': cvemploy,
            'user_cv_status': data.usercv.user_cv_builder_status,
            'body_status': 0
        })

    def post(self, request):
        data = UserEmployment.objects.filter(user_id=request.user.id, id=request.POST['employment_id'])[0]
        employee_data = {
            'company_name': data.company_name,
            'company_work_title': data.company_worktitle,
            'company_from': str(data.company_from),
            'company_to': str(data.company_to),
            'company_description': data.company_description,
        }
        return HttpResponse(json.dumps({'data': employee_data}))


def edit_company_description(request):
    data = UserEmployment.objects.filter(id=request.POST['job_employment_id']).update(
        company_worktitle=request.POST['company_worktitle'],
        company_name=request.POST['company_name'],
        company_to=request.POST['company_to'],
        company_from=request.POST['company_from']
    )
    return HttpResponse(json.dumps({'status':True}))


def delete_company_description(request):
    data = UserEmployment.objects.filter(user_id=request.user.id, id=request.POST['employment_id']).delete()
    return HttpResponse(json.dumps({'status':True}))


class ProfileSettingsResume(View):
    @method_decorator(login_required)
    @method_decorator(is_job_seeker)
    def get(self, request):
        user_cv = UserCV.objects.filter(user_id=request.user.id)[0]
        return render(request, 'profile_settings_resume.html',{
            'user_cv':user_cv,
            'user_cv_status': user_cv.user_cv_builder_status,
            'body_status': 0
        })

    def post(self, request):
        if request.FILES:
            get_user = UserCV.objects.filter(user_id=request.user.id)[0]
            get_user.user_cv_title = request.FILES['resume_file'].name
            get_user.user_cv_file = request.FILES['resume_file']
            get_user.save()
            return HttpResponse(json.dumps({'status':True}));
        else:
            return HttpResponseRedirect('/user/u/profile_settings/resume/')

class UserMessages(View):
    @method_decorator(login_required())
    @method_decorator(is_job_seeker)
    def get(self, request):
        print request.user.id
        list_users = company_models.Messages.objects.raw(
            """
             SELECT * from company_messages join auth_user ON auth_user.id = company_messages.sender_id
             where receiver_id={0}
             group by auth_user.id order by company_messages.date_send
            """.format(request.user.id)
        )


        # totalnumber = company_models.Messages.objects.raw(
        #     """
        #      SELECT * from company_messages join auth_user ON auth_user.id = company_messages.sender_id
        #      where receiver_id={0}
        #      group by auth_user.id order by company_messages.date_send
        #     """.format(request.user.id)
        # )


        # print list_users[0].message_body
        try:
            print list_users[0] # To check if the user exists or not
            print list_users[0].receiver_id
        except IndexError:
            print "omer"
            return render(request, 'user_message_none.html')

        if list_users[0].receiver_id == request.user.id:
            candidate_id = list_users[0].sender_id
        else:
            candidate_id = list_users[0].receiver_id
        print candidate_id, request.user.id
        data = get_user_messages(candidate_id,request.user.id)
        return render(
            request,
            'user_message.html',
            {
                'list': list_users,
                'message_data': data['all_data_sort'],
                'sender_side_name': data['server_side_name'],
                'sender_id': request.user.id,
                'candidate_id': candidate_id,
                'body_status': 0
            }
        )


    def post(self, request):
        """

        """


class UserSendMessage(View):
    def get(self, request):
        print 'ola'
    def post(self, request):
        company_models.Messages(
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


class UserComposedSend(View):
    def get(self, request):
        print 'ola'
    def post(self, request):
        company_models.Messages(
            message_title=request.POST['subject_message'],
            receiver_id=int(request.POST['candidate_id']),
            sender_id=request.user.id,
            message_body=request.POST['content_message'],
            date_send=datetime.now()
        ).save()
        obj = company_models.Messages.objects.latest('id')
        print obj
        html = render_to_string('company_message_send.html', {'message': obj} )
        return HttpResponse(
            html
        )


def get_user_messages(candidate_id, user_id):
        print "omer omer"
        data_sender_side = company_models.Messages.objects.filter(
            sender_id=user_id,
            receiver_id=candidate_id
        ).prefetch_related(
            'sender'
        ).order_by('date_send') # Sender messages to the receiver
        print data_sender_side
        data_receiver_side = company_models.Messages.objects.filter(
            sender_id=candidate_id,
            receiver_id=user_id
        ).prefetch_related(
            'receiver'
        ).order_by('date_send') # Which receiver sends the message to the sender
        print data_receiver_side
        # merging the two models instances
        if data_receiver_side:
            if data_sender_side:
                # Both sender and receiver side is available
                all_data_sort = sorted(chain(
                    data_sender_side, data_receiver_side
                ),key=lambda message_data: message_data.date_send, reverse=False)
            else:
                # If the data sender side is empty
                all_data_sort = sorted(
                data_receiver_side,
                key=lambda message_data: message_data.date_send,
                reverse=False
            )

        else:
            # if the data receiver type is empty
            all_data_sort = sorted(
                data_sender_side,
                key=lambda message_data: message_data.date_send,
                reverse=False
            )
        # receiver sending the message to the sender.
        # If the data sender is empty then use the data receiver
        if data_sender_side:
            sender_side_name = data_sender_side[0].receiver.first_name + " " + data_sender_side[0].receiver.last_name
        else:
            sender_side_name = data_receiver_side[0].sender.first_name + " " + data_receiver_side[0].sender.last_name
        data_value = {
            'all_data_sort': all_data_sort,
            'server_side_name': sender_side_name
        }
        return data_value


# Job alert section

class JobAlertView(View):
    def get(self, request):
        """

        :param request:
        :return:
        """

    def post(self, request):
        try:
            data = JobAlert.objects.get_or_create(user_id=request.user.id, category_id=request.POST['category_id'])
            get_category_name = core_models.Categories.objects.getinfo(request.POST['category_id'])

            if data[1]:
                listvalue = {
                    'tosend': User.objects.filter(id=request.user.id)[0].email,
                    'username': User.objects.filter(id=request.user.id)[0].username,
                    'first_name': User.objects.filter(id=request.user.id)[0].first_name,
                    'message': get_category_name[0].category_name
                }
                sendemail_ = email.EmailFunc('job_alert_email', **listvalue)
                sendemail_.generic_email()
                return HttpResponse(json.dumps({'status':True}))
            else:
                return HttpResponse(json.dumps({'status':False}))
        except MultipleObjectsReturned:
            return HttpResponse(json.dumps({'status':False}))



