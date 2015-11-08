import simplejson as json

from django.shortcuts import render
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

from accounts import models as accountsmodels
from accounts import forms as accountsform
from company import models as company_models
from core.decoraters import *
from core import models as core_models

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
        if step_value == '0':
            detect_user = UserSkills.objects.filter(user_id=request.user.id)
            if detect_user:
                return HttpResponseRedirect('/user/create-basic-profile/?step=1')
            cats = list_categories.list_categories()
            return render(
                request,
                'user_selection.html',
                {
                    'categories':cats
                }
            )

        if step_value == '1':
            userProfile = UserBioInfo()
            userLocation = UserLocationForm()
            detect_user = UserBio.objects.filter(user_id=request.user.id)
            if detect_user:
                return HttpResponseRedirect('/user/create-basic-profile/?step=2')
            return render(request, 'user_biography.html', {'userbio': userProfile, 'userloc': userLocation})

        if step_value == '2':

            user_status = accountsmodels.UserProfile.objects.filter(
                    user_id=request.user.id
                )[0]
            print 'dsadas%s' %user_status


            user_cv_data = cv_object_ret(request.user.id)

            if user_cv_data:    # user CV table status should be 0 and user profile status should be 0
                if user_cv_data.user_cv_builder == 0 or user_status.user_cv_status == 1:
                        return HttpResponseRedirect('/user/create-basic-profile/?step=3')
            cvform = UserCVForm()
            return render(request, 'cv_selection_page.html', {'user_cv_form': cvform})

        if step_value == '3':
            user_cv = UserCV.objects.filter(user_id=request.user.id)[0]

            if user_cv.user_cv_emp_status == 0:

                cvemploy = InitialEmploymentForm()
                return render(request, 'user_employment.html', {'cv_employ': cvemploy})

            if user_cv.user_cv_emp_status == 1 and user_cv.user_cv_builder==0:
                return HttpResponseRedirect('/user/dashboard/')


        if step_value == '4':
            user_cv_data = cv_object_ret(request.user.id)
            if user_cv_data.user_cv_builder == 0:
                return HttpResponseRedirect('/user/dashboard/')
            elif user_cv_data.user_cv_builder==1:
                """
                CV builder further detials include
                user_graduation status along with other info.
                """
                return HttpResponseRedirect('/user/education/')
    else:
        HttpResponseRedirect('/accounts/signup/confirm-email')



class UserDashboard(View):

    @method_decorator(login_required)
    def get(self, request):
        jobs_details = company_models.Advertisement.admanager.filter(job_approval_status=1).order_by('-submission_date')[:5]
        applied_jobs = company_models.AdvertisementApplied.objects.filter(user_id=request.user.id).count()
        # shortlisted_jobs =
        favorite_jobs = company_models.AdvertisementFavorite.objects.filter(user_id=request.user.id).count()
        return render(
            request,
            'profile_dashboard.html',
            {
                'job_detail': jobs_details,
                'applied_jobs': applied_jobs,
                'favorite_jobs': favorite_jobs
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
                user_bio = UserBio()
                user_bio.user = User.objects.filter(id=request.user.id)[0]
                user_bio.user_bio_status = 1
                user_bio.user_portrait = request.FILES['user_portrait']
                user_bio.user_title = request.POST['user_title']
                user_bio.user_overview = request.POST['user_overview']
                user_bio.user_language_pre = request.POST['user_language_pre']
                ret = user_bio.save()
                # storing user location details
                user_location = UserLocation(
                    user_address = request.POST['user_address'],
                    user_city = request.POST['user_city'],
                    user_country = request.POST['user_country'],
                    user_zipcode = request.POST['user_zipcode'],
                    user_phone_no = request.POST['user_phone_no'],
                    user_location_status = 1,
                    user = User.objects.filter(id=request.user.id)[0]

                )
                user_location.save()

                return HttpResponse(json.dumps({'status': True}))


class UserCVUpload(View):
    """
    Uploading user cv through it
    """
    @method_decorator(login_required)

    def get(self, request, *args, **kwargs):
        """
        """
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
                accountsmodels.UserProfile.objects.filter(
                    user_id=request.user.id
                ).update(
                    user_cv_status=1
                )
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
    Updating user employment
    """
    @method_decorator(login_required)
    def get(self, request):
        """
        """
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        """
        count_check = len(request.POST.getlist('company_name'))

        try:
            for ab in range(0, count_check):
                c_worktitle = request.POST.getlist('company_worktitle')[ab]
                c_name = request.POST.getlist('company_name')[ab]
                c_location = request.POST.getlist('company_location')[ab]
                c_role = request.POST.getlist('company_role')[ab]
                c_from = request.POST.getlist('company_from')[ab]
                c_to = request.POST.getlist('company_to')[ab]
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
                )
                user.save()
                UserCV.objects.filter(user_id=request.user.id).update(
                    user_cv_emp_status=1
                )

        except:
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
        """
        """
        if request.method=='POST':
            count_check = len(request.POST.getlist('user_institute'))
            print count_check
            print request.POST.getlist('user_institute')
            try:
                for ab in range(0, count_check):
                    user_institute = request.POST.getlist('user_institute')[ab]
                    user_degree = request.POST.getlist('user_degree')[ab]
                    degree_from = request.POST.getlist('degree_from')[ab]
                    degree_to = request.POST.getlist('degree_to')[ab]
                    # c_description = request.POST.getlist('company_description')[ab]
                    user = UserEducation(
                        user_id=request.user.id,
                        user_institute=user_institute,
                        user_degree=user_degree,
                        degree_from=degree_from,
                        degree_to=degree_to,
                        # company_description =,
                    )
                    user.save()
                    UserCV.objects.filter(user_id=request.user.id).update(
                        user_cv_education=1
                    )
            except Exception as e:
                print e

    def show_form(self, request):
        EduForm = EducationForm()
        return render(request, 'profile_education.html', {'edu': EduForm})



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
        return render(request, 'user_profile.html', {'user_basic_form': user_basic})

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
        return render(request, 'user_change_password.html', {'cp': change_password})

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
        country = core_models.Countries.objects.filter(id=data.userlocation.user_country)[0]
        city = core_models.Cities.objects.filter(id=data.userlocation.user_city)[0]
        education = UserEducation.objects.filter(user_id=request.user.id)
        main = {
            'first_name': data.first_name,
            'last_name': data.last_name,
            'overview': data.userbio.user_overview,
            'email': data.email,
            'contact': data.userlocation.user_phone_no,
            'address': data.userlocation.user_address,
            'portrait': portrait,
            'country': country.country_name,
            'city': city.city_name
        }
        print main
        return render(request, 'profile.html', {
            'user': main,
            'user_employment': employment_data,
            'user_education': education
        })

class ProfileSettings(View):
    @method_decorator(login_required)
    @method_decorator(is_job_seeker)
    def get(self, request):
        data = User.objects.prefetch_related('userbio','usercv','userskills', 'userlocation').get(id=request.user.id)
        employment_data =UserEmployment.objects.filter(user_id=request.user.id)
        portrait = str(data.userbio.user_portrait)
        portrait = portrait[portrait.find('/media'):]
        country = core_models.Countries.objects.filter(id=data.userlocation.user_country)[0]
        city = core_models.Cities.objects.filter(id=data.userlocation.user_city)[0]
        education = UserEducation.objects.filter(user_id=request.user.id)


        main = {
            'first_name': data.first_name,
            'last_name': data.last_name,
            'overview': data.userbio.user_overview,
            'email': data.email,
            'contact': data.userlocation.user_phone_no,
            'address': data.userlocation.user_address,
            'portrait': portrait,
            'country': country.country_name,
            'city': city.city_name
        }
        print main
        return render(request, 'profile_settings.html', {
            'user': main,
            'user_employment': employment_data,
            'user_education': education
        })


