import simplejson as json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django import views
from models import *
from forms import *
from django.views.generic import View
from accounts import models as accountsmodels


# Create your views here.
def index(request):
    """
    Whole view for the company - starting out from the selection of the website.
    """
    step_value = request.GET.get('step', '')
    list_categories = UserSkills()
    if request.user.is_active:
        # print request.
        # detect_already_Exit
        # Skillsobj = UserSkills()
        if UserSkills.objects.exist_not(request.user.id):
            HttpResponseRedirect('/user')   # later on have to change the request
        if step_value == '0':
            detect_user = UserSkills.objects.filter(user_id=request.user.id)
            if detect_user:
                return HttpResponseRedirect('/user/create-basic-profile/?step=1')
            cats = list_categories.list_categories()
            return render(request, 'user_selection.html', {'categories':cats})

        if step_value == '1':
            userProfile = UserBioInfo()
            detect_user = UserBio.objects.filter(user_id=request.user.id)
            if detect_user:
                return HttpResponseRedirect('/user/create-basic-profile/?step=2')
            return render(request, 'user_biography.html', {'userbio': userProfile})

        if step_value == '2':
            user_status = accountsmodels.UserProfile.objects.filter(
                    user_id=request.user.id
                )[0]

            try:
                user_cv_data = UserCV.objects.filter(user_id=request.user.id)[0]
            except IndexError:
                user_cv_data = False

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


    else:
        HttpResponseRedirect('/accounts/signup/confirm-email')


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


class UserInfo(View):
    """
    This section includes the user biography and CV builder.
    """



    def post(self, request, *args, **kwargs):
        """
        Handling the user basic profile information
        """
        detect_user = UserBio.objects.filter(user_id=request.user.id)
        if detect_user:
            return HttpResponse(json.dumps({'status': True}))
        if request.method == 'POST':
            form = UserBioInfo(request.POST, request.FILES)
            print form
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
                return HttpResponse(json.dumps({'status': True}))


class UserCVUpload(View):

    def get(self, request, *args, **kwargs):
        """
        """

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
                print 'user account updated!'




def AddCVEmployment(request):

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


    def get(self, request):
        """
        """

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


class UserBioUpdate(View):

    def get(self, request, *args, **kwargs):
        """
        """

    def post(self, request, *args, **kwargs):
        """
        """