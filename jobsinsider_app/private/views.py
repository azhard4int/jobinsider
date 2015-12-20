from django.shortcuts import render, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from .forms import *
from .models import *
from django.db import models
from django.core import serializers
from django.template import context, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from urlparse import urlparse, parse_qs

from evaluation.models import *
from core import models as modeinsert
from company import models as company_model
from company import forms as company_forms
from advertisement import AdvertisementAdminView

from django.db import models
from accounts import models as accounts_models
from users import models as user_models
from django.db.models.query import RawQuerySet

import simplejson as json
from datetime import *
import time

# Create your views here.
@login_required()
def index(request):
    return HttpResponse('Logged in as Administrator')


@login_required()
def login_admin_view(request):
    """
    Only for the administrator privilleged users.
    """

    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user.is_superuser:
            login(request, user)
            return HttpResponseRedirect('/private/members/')
        else:
            return HttpResponseRedirect('/private/')

    else:
        admin = Adminlogin()
        return render(request, 'admin_login.html', {'admin_form': admin})

@login_required()
def members_view(request):
    """
    For administrator based users to show them the data
    """
    user = UsersAccounts()
    user_accounts = user.list_all()
    print user_accounts
    return render(request, 'list.html', {'listusers': user_accounts})


"""
Categories Views includes:
Add
Edit
Delete
Update Status
"""


@login_required()
def categories_view(request):
    """
    For categories list view
    """
    catObj = CategoriesInstance()  # instance created from the class model.
    categories_list = catObj.list_all()    # returns all items in list view
    count_item = catObj.count_items()  # returns total items

    addCatForm = CategoryAdd()

    return render(request, 'list_categories.html', {
        'catlist': categories_list,
        'count_category': count_item,
        'add_category': addCatForm
    })


@login_required()
def categories_add(request):
    """
    For adding new categories.
    """
    return render()

@login_required()
def process_catadd(request):

    print request.FILES
    if request.method=='POST':
        category_status = request.POST['category_status']
        category_name = request.POST['category_name']
        category_image = request.FILES['category_image']
        filename = request.FILES['category_image'].name
        catInstance = modeinsert.Categories(
            category_status=category_status,
            category_name=category_name,
            category_image=category_image,
            file_name=filename
        )
        catInstance.save()
        return HttpResponse(json.dumps({'status': 1}))


def process_enable_status(request):
    """
    Updating the category status
    """
    cat_id = request.GET.get('cat_id', '')
    if modeinsert.Categories.objects.enable_category(cat_id):
        return HttpResponse(json.dumps({'status': 'True'}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))


def process_disable_status(request):
    """
    Updating the category status
    """
    cat_id = request.GET.get('cat_id', '')
    if modeinsert.Categories.objects.disable_category(cat_id):
        return HttpResponse(json.dumps({'status': 'True'}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))


def process_delete_status(request):
    """
    Updating the category status
    """
    cat_id = request.GET.get('cat_id', '')
    if modeinsert.Categories.objects.delete_category(cat_id):
        return HttpResponse(json.dumps({'status': 'True'}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))


def process_cat_details(request):
    """
    Getting the list details of skills
    """
    category_id_value = request.GET.get('cat_id', '')
    get_cat_detail = modeinsert.Skills.listall(category_id_value)
    if get_cat_detail:
        return HttpResponse(json.dumps({'status': 'True', 'skills': get_cat_detail}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))

@login_required()
def process_edit_form(request, editid):


    data = modeinsert.Categories.objects.getinfo(editid)
    if data:
        # print data
        cat_form = CategoryEdit(initial={
                'category_status': data[0].category_status,
                'category_name': data[0].category_name,
                'id': data[0].id
            })

        data_still = modeinsert.Skills.objects.listall(data[0].id)
        print data_still
        return render(request, 'edit_category.html', {'editform': cat_form, 'list_skills': data_still})

@login_required()
def process_category_edit(request):
    if request.method == 'POST':
        data = modeinsert.Categories.objects.filter(id=request.POST['id']).update(
            category_name=request.POST['category_name'],
            category_status=request.POST['category_status'])
        return HttpResponseRedirect('/members/')
        if data:
            return HttpResponse(json.dumps({'status': 'True'}))
        else:
            return HttpResponse(json.dumps({'status': 'False'}))

@login_required()
def skills_view(request, edit):

    data = modeinsert.Skills.objects.getinfo(edit)
    if data:
        # print data
        editForm = EditSkill(initial={
                    'skill_status': data[0].skill_status,
                    'skill_name': data[0].skill_name,
                    'id': data[0].id
                })

        return render(request, 'edit_skill.html', {'editform': editForm})


def skill_view_enable(request):
    skillObj = modeinsert.Skills.objects.enable_status(request.POST['skill_id'])
    if skillObj:
        return HttpResponse(json.dumps({'status': 'True'}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))


def skill_view_disable(request):
    skillObj = modeinsert.Skills.objects.disable_status(request.POST['skill_id'])
    if skillObj:
        return HttpResponse(json.dumps({'status': 'True'}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))

def skill_view_delete(request):
    skillObj = modeinsert.Skills.objects.delete_status(request.POST['skill_id'])
    if skillObj:
        return HttpResponse(json.dumps({'status': 'True'}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('http://127.0.0.1:8000/accounts/login/')

from itertools import chain

@login_required()
def users_view(request):

    # table2 = User.objects.filter(userprofile__user_id=x)
    # table2 = accounts_models.UserProfile.objects.all().prefetch_related('user_id')
    # table = User.objects.filter(id=table2)
    # print table
    query = "SELECT * From auth_user JOIN accounts_userprofile on auth_user.id=accounts_userprofile.user_id"
    table = User.objects.raw(query)
    paginator = Paginator((list(table)),25) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        table = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        table = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        table = paginator.page(paginator.num_pages)
    # return render_to_response('list.html', {"contacts": contacts})
    return render(request, 'users_view.html',{'table':table})


class User_View(View):

    def get(self,request):
        query = "SELECT * From auth_user JOIN accounts_userprofile on auth_user.id=accounts_userprofile.user_id"
        table =  User.objects.raw(query)


        paginator = Paginator((list(table)), 25) # Show 25 contacts per page

        page = request.GET.get('page')
        try:
           table = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
           table = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            table = paginator.page(paginator.num_pages)

    # return render_to_response('list.html', {"contacts": contacts})
        return render(request, 'users_view.html',{'table':table})



@login_required()
def test_userinfo(request):
    data = User.objects.get(id=request.POST.get('user_id',''))
    wholedata = {

        'firstname': data.first_name,
        'lastname': data.last_name,
        'username': data.username,
        'email': data.email,
        'status' : data.is_active,
        'staff':data.is_staff,
        'superuser': data.is_superuser
    }
    return HttpResponse(json.dumps({'user_info': wholedata}))


@login_required()
def user_update(request):
    if request.method=='POST':
        print request.POST['is_active']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        is_active = request.POST['is_active']
        staff = request.POST['is_staff']
        superuser = request.POST['is_superuser']

        data = User.objects.filter(id=request.POST['id']).update(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=int(is_active),
            is_staff=int(staff),
            is_superuser=int(superuser))

        try:
           data2 = accounts_models.UserProfile.objects.filter(user_id=request.POST['id']).update(user_status=request.POST['profile_status'])

           if not data2:
            data3 = accounts_models.UserProfile(user_id=request.POST['id'], user_status=request.POST['profile_status'])
            data3.save()

        except Exception as ae:
            data3 = accounts_models.UserProfile(user_id=request.POST['id'], user_status=request.POST['profile_status'])
            data3.save()


    if data:
        return HttpResponse(json.dumps({'status': 'True'}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))

@login_required()
def user_add(request):
    if request.method=='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = 123456789
        status= request.POST['profile_status']
    if User.objects.filter(email=request.POST['email']).exists() or User.objects.filter(username=request.POST['username']).exists() is True:
        return HttpResponse(json.dumps({'status': 'Email or user exist'}))
    else:
        data = User(username=username,first_name=first_name,last_name=last_name,email=email,password = password)
        data.save()


    result = User.objects.get(email=email)

    whole = {
      'id': result.id,
      'firstname': result.first_name,
      'lastname': result.last_name,
      'username': result.username,
      'email': result.email,
      'active' : result.is_active
    }
    #this is for adding userprofile and updating user_status
    data2 = accounts_models.UserProfile(user_id=result.id, user_status=status)
    data2.save()

    if data and result:
        return HttpResponse(json.dumps({'status': 'True','info': whole}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))


@login_required()
def user_delete(request):
    if request.method=='POST':
        id = request.POST['id']
    data=User.objects.filter(id=int(id)).delete()
    if data:
        return HttpResponse(json.dumps({'status': 'True'}))
    else:
        return HttpResponse(json.dumps({'status': 'False'}))

@login_required()
def user_search(request):
    value = request.POST['value']
    if request.method=='POST':
            try:
              firstname=User.objects.filter(first_name=value)
              wholedata = serializers.serialize('json', firstname)
              if firstname:
                 return HttpResponse(json.dumps({'user_info': wholedata}))
            except Exception as e:
                     print e

            try:
              user123=User.objects.filter(username=value)
              wholedata = serializers.serialize('json', user123)
              if user123:
                 return HttpResponse(json.dumps({'user_info': wholedata}))
            except Exception as e:
                 print e



            try:
              email123=User.objects.filter(email=value)
              wholedata = serializers.serialize('json', email123)
              if email123:
                 return HttpResponse(json.dumps({'user_info': wholedata}))
            except Exception as ae:
               print ae



            try:
              lastname=User.objects.filter(last_name=value)
              wholedata = serializers.serialize('json', lastname)
              if lastname:
                 return HttpResponse(json.dumps({'user_info': wholedata}))
            except Exception as ee:
               print ee


    return HttpResponse(json.dumps({'status': 'Not Found'}))


@login_required()
def get_id(request):
         data = User.objects.get(username=request.POST.get('username'))
         wholedata = {

           'id': data.id
           }
         return HttpResponse(json.dumps({'user_info': wholedata}))


@login_required()
def allusers(request):
         try:
            data=User.objects.all().order_by('-date_joined')

            wholedata = serializers.serialize('json', data)
            if data:
                return HttpResponse(json.dumps({'user_info': wholedata}))
         except Exception as e:
                 print e

@login_required()
def activeusers(request):
        query = "SELECT * From auth_user JOIN accounts_userprofile on auth_user.id=accounts_userprofile.user_id Where auth_user.is_active=1"
        table =  User.objects.raw(query)
        table2 = pagination_table(request.GET.get('page'),table)
        return render(request, 'users_view.html',{'table':table2})

@login_required()
def nonactiveusers(request):
        try:
            query = "SELECT * From auth_user JOIN accounts_userprofile on auth_user.id=accounts_userprofile.user_id Where auth_user.is_active=0"

            table =  User.objects.raw(query)

            # data=User.objects.filter(is_active=0).order_by('date_joined')
            table2 = pagination_table(request.GET.get('page'),table)

            if table and table2:
                return render(request, 'users_view.html',{'table':table2})

        except Exception as e:
               return render(request, 'users_view.html',{'status':'False'})



@login_required()
def getprofilestatus(request):

    if request.method=='POST':
       value = request.POST['id']
    try:
        data=accounts_models.UserProfile.objects.get(user_id=value)
        wholedata = {
             'user_status':data.user_status

            }
        if data:
           return HttpResponse(json.dumps({'user_info': wholedata}))
        else:
            return HttpResponse(json.dumps({'status': 'False'}))

    except Exception as e:
          return HttpResponse(json.dumps({'user_info': 'Notdefined'}))

@login_required()
def companyfilter(request):
         try:
            # data=User.objects.all().filter(userprofile__user_status=0)
            query = "SELECT * From auth_user JOIN accounts_userprofile on auth_user.id=accounts_userprofile.user_id Where accounts_userprofile.user_status=1 ORDER BY date_joined"
            table =  User.objects.raw(query)
            # data=User.objects.filter(is_active=0).order_by('date_joined')
            table2 = pagination_table(request.GET.get('page'),table)

            if table and table2:
                return render(request, 'users_view.html',{'table':table2})

         except Exception as e:
               return HttpResponse(json.dumps({'status': 'False'}))

@login_required()
def job_seekerfilter(request):
         try:
            # data=User.objects.all().filter(userprofile__user_status=0)
            query = "SELECT * From auth_user JOIN accounts_userprofile on auth_user.id=accounts_userprofile.user_id Where accounts_userprofile.user_status=0 ORDER BY date_joined"
            table =  User.objects.raw(query)
            # data=User.objects.filter(is_active=0).order_by('date_joined')
            table2 = pagination_table(request.GET.get('page'),table)

            if table and table2:
                return render(request, 'users_view.html',{'table':table2})

         except Exception as e:
               return HttpResponse(json.dumps({'status': 'False'}))
# @login_required()
# def job_seekerfilter(request):
#          try:
#             # data=User.objects.select_related('userbio').get(id=98)
#             # data=User.objects.select_related('userbio').get(id=98)
#             # data=User.objects.all().prefetch_related('userbio')
#             # data = User.objects.prefetch_related('userbio__userskill'). get(id=98)
#             #  data = User.objects.select_related('userbio','userskills').get(id=98)
#
#             # data = User.objects.filter(id=98).prefetch_related('userbio')
#             #  data =
#             # data= User_models.useremployment.objects.get(id=98)
#             hell=User.objects.prefetch_related('userbio','usercv','userlocation','userskills').get(id=98)
#             data=user_models.UserEmployment.objects.get(user_id=98)
#             print data.company_name
#             print hell.userbio.user_id
#             print hell.usercv.user_id
#
#
#             # data = User.objects.select_related('useremployment').get(id=98)
#             # data = User.objects.select_related('useremployment').filter(user_id=98)
#
#
#             # print data.useremployment.user_id
#             # print data.userskills
#             # print data.userbio.user_id
#             # print data.usercv.user_id
#             # print data.useremployment.user_address
#
#             # wholedata = serializers.serialize('json', data)
#             # if data:
#             #     return HttpResponse(json.dumps({'user_info': wholedata}))
#             # else:
#             #     return HttpResponse(json.dumps({'status': 'False'}))
#             if data:
#                     return HttpResponse(json.dumps({'user_info': 'True'}))
#             else:
#                    return HttpResponse(json.dumps({'status': 'False'}))
#          except Exception as e:
#                  print "Error aagaya hai manhoos"


@login_required()
def profile_full(request):
   if request.method=='POST':
     value = request.POST['id']
     try:
        hell=User.objects.prefetch_related('userbio','usercv','userlocation','userskills').get(id=value)
        hell2=user_models.UserEmployment.objects.get(user_id=value)
        picture =str(hell.userbio.user_portrait)
        wholedata = {
            'name' : hell.first_name,
            'last':hell.last_name,
            'email':hell.email,
            'contact':hell.userlocation.user_phone_no,
            'address':hell.userlocation.user_address,
            'exp':hell2.company_name,
            'pic':picture
        }
        print wholedata
        if hell and hell2:
           return HttpResponse(json.dumps({'user_info': wholedata}))
        else:
            return HttpResponse(json.dumps({'status': 'False'}))
     except Exception as e:
           return HttpResponse(json.dumps({'status': 'False'}))

@login_required()
def skill_add(request):
    if request.method=='POST':
        modeinsert.Skills(
            category_id=request.POST['cat_id'],
            skill_name=request.POST['skill_value'],
            skill_status=1
        ).save()
        return HttpResponse(json.dumps({'status':True}))


class EducationView(View):
    @method_decorator(login_required)
    def get(self, request):
        eduForm = EducationForm()
        list_all = modelf.Education.objects.all()
        return render(request, 'list_education.html', {'edu': eduForm, 'edu_list':list_all})

    def post(self, request):
        modelf.Education(
            education_name=request.POST['education_name']
        ).save()
        return HttpResponse(json.dumps({'status':True}))


def education_delete(request):
    if request.method=='POST':
        modelf.Education.objects.filter(id=request.POST['education_id']).delete()
        return HttpResponse(json.dumps({'status':True}))

def education_enable(request):
    if request.method=='POST':
        modelf.Education.objects.filter(id=request.POST['education_id']).update(education_status=1)
        return HttpResponse(json.dumps({'status':True}))

def education_disable(request):
    if request.method=='POST':
        modelf.Education.objects.filter(id=request.POST['education_id']).update(education_status=0)
        return HttpResponse(json.dumps({'status':True}))

def education_edit(request):
    if request.method=='POST':
        print request.POST['status']
        if request.POST['status']=='0':
            edu_id = modelf.Education.objects.filter(id=request.POST['education_id'])[0]
            return HttpResponse(json.dumps({'edu_id':edu_id.education_name}))
        else:
            modelf.Education.objects.filter(id=request.POST['education_id']).update(
                education_name=request.POST['edit_education_name']
            )
            return HttpResponse(json.dumps({'edu_id':True}))


class ExperienceView(View):
    @method_decorator(login_required)
    def get(self, request):
        expForm = ExperienceForm()
        list_all = company_model.Experience.objects.all()
        return render(request, 'list_experience.html', {'exp': expForm, 'exp_list':list_all})

    def post(self, request):
        company_model.Experience(
            experience_name=request.POST['experience_name']
        ).save()
        return HttpResponse(json.dumps({'status':True}))


def experience_delete(request):
    if request.method=='POST':
        company_model.Experience.objects.filter(id=request.POST['experience_id']).delete()
        return HttpResponse(json.dumps({'status':True}))

def experience_enable(request):
    if request.method=='POST':
        company_model.Experience.objects.filter(id=request.POST['experience_id']).update(experience_status=1)
        return HttpResponse(json.dumps({'status':True}))

def experience_disable(request):
    if request.method=='POST':
        company_model.Experience.objects.filter(id=request.POST['experience_id']).update(experience_status=0)
        return HttpResponse(json.dumps({'status':True}))

def experience_edit(request):
    if request.method=='POST':
        print request.POST['status']
        if request.POST['status']=='0':
            exp_id = company_model.Experience.objects.filter(id=request.POST['experience_id'])[0]
            return HttpResponse(json.dumps({'exp_id':exp_id.experience_name}))
        else:
            company_model.Experience.objects.filter(id=request.POST['experience_id']).update(
                experience_name=request.POST['edit_experience_name']
            )
            return HttpResponse(json.dumps({'exp_id':True}))


class EmploymentView(View):
    @method_decorator(login_required)
    def get(self, request):
        expForm = EmploymentForm()
        list_all = company_model.Employment.objects.all()
        return render(request, 'list_empoyment.html', {'emp': expForm, 'emp_list':list_all})

    def post(self, request):
        company_model.Employment(
            employment_name=request.POST['employment_name']
        ).save()
        return HttpResponse(json.dumps({'status':True}))


def employment_delete(request):
    if request.method=='POST':
        company_model.Employment.objects.filter(id=request.POST['employment_id']).delete()
        return HttpResponse(json.dumps({'status':True}))

def employment_enable(request):
    if request.method=='POST':
        company_model.Employment.objects.filter(id=request.POST['employment_id']).update(employment_status=1)
        return HttpResponse(json.dumps({'status':True}))

def employment_disable(request):
    if request.method=='POST':
        company_model.Employment.objects.filter(id=request.POST['employment_id']).update(employment_status=0)
        return HttpResponse(json.dumps({'status':True}))

def employment_edit(request):
    if request.method=='POST':
        print request.POST['status']
        if request.POST['status']=='0':
            emp_id = company_model.Employment.objects.filter(id=request.POST['employment_id'])[0]
            return HttpResponse(json.dumps({'emp_id':emp_id.experience_name}))
        else:
            modelf.Employment.objects.filter(id=request.POST['employment_id']).update(
                employment_name=request.POST['edit_employment_name']
            )
            return HttpResponse(json.dumps({'emp_id':True}))


#evaluation part starts from here------------------------>

def evaluation_index(request):
    try:
       table = evaluation_test_template.objects.filter(evaluation_status=0).exclude(user_id=14)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin.html',{'status':'Falses'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def evaluation_default(request):
    try:
       table = evaluation_test_template.objects.all()
       print table
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin_default.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin_default.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def evaluation_user(request):
    try:
       table = evaluation_test_template.objects.filter(evaluation_status=1)
       # query2 = "SELECT * From auth_user JOIN evaluation_test_template on auth_user.id=evaluation__evaluation_test_template.user_id WHERE evaluation__evaluation_status=1"
       # table =  User.objects.raw(query2)
       print table

       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin_approved.html',{'evaluation':table})
       else:
           return render(request, 'evaluation_index_admin_approved.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def evaluation_user_pending(request):
    try:
       table = evaluation_test_template.objects.filter(evaluation_status=0)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def evaluation_user_approved(request):
    try:
       table = evaluation_test_template.objects.filter(evaluation_status=1)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def evaluation_user_rejected(request):
    try:
       table = evaluation_test_template.objects.filter(evaluation_status=2)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin_rejected.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin_rejected.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def edit_evaluation_question(request,id):
    try:
         query=evaluation_test_questions.objects.filter(evaluation_test_template_id=id)
         if query:
            return render(request, 'evaluation_edit_questions_admin.html',{'query':query})

         else:return render(request, 'evaluation_edit_questions_admin.html')


    except Exception as e:
            return render(request, 'evaluation_edit_questions_admin.html')


def addtemplate(request):
        try:

           query=evaluation_test_template(
                evaluation_name=request.POST['evaluation_name'],
                evaluation_description=request.POST['evaluation_description'],
                evaluation_catagory=request.POST['evaluation_catagory'],
                evaluation_rules=request.POST['evaluation_rules'],
                evaluation_status=1,
                evaluation_type=int(request.POST['evaluation_type']),
                evaluation_time=int(request.POST['evaluation_time']),
                evaluation_total_questions=int(request.POST['evaluation_questions']),
                user_id=14
           )
           query.save()
           obj = evaluation_test_template.objects.latest('id')

           whole = {
               'evaluation_id':obj.id,
               'evaluation_name':request.POST['evaluation_name'],
               'evaluation_catagory':request.POST['evaluation_catagory'],
               'evaluation_status':0,
               'evaluation_type':(request.POST['evaluation_type']),
               'evaluation_total_questions':(request.POST['evaluation_questions'])
           }

           if query:
                 return HttpResponse(json.dumps({'status': whole}))
           else:
                 return HttpResponse(json.dumps({'status': 'False'}))

        except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': 'Err'}))




def approve_evaulation(request):
    try:
        query = evaluation_test_template.objects.filter(id=request.POST['id']).update(evaluation_status=1)

        if query:
             return HttpResponse(json.dumps({'status': 'True'}))
        else:
             return HttpResponse(json.dumps({'status': 'False'}))

    except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': 'Err'}))

def reject_evaulation(request):
    try:
        query = evaluation_test_template.objects.filter(id=request.POST['id']).update(evaluation_status=2)

        if query:
             return HttpResponse(json.dumps({'status': 'True'}))
        else:
             return HttpResponse(json.dumps({'status': 'False'}))

    except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': 'Err'}))



def edit_user_template_by_admin(request):
         try:
             query = evaluation_test_template.objects.filter(id=request.GET['id'])
             list= {
                 'id':query[0].id,
                 'evaluation_name':query[0].evaluation_name,
                 'evaluation_description':query[0].evaluation_description,
                 'evaluation_rules':query[0].evaluation_rules,
                 'evaluation_catagory':query[0].evaluation_catagory,
                 'evaluation_type':query[0].evaluation_type,
                 'evaluation_time':query[0].evaluation_time,
                 'evaluation_total_questions':query[0].evaluation_total_questions

              }
             if query:
                return HttpResponse(json.dumps({'status': list}))
             else:
                 return render(request, 'Error')

         except Exception as e:
            print e

         return HttpResponse(json.dumps({'status': 'Err'}))

def pagination_table(page,table):
        paginator = Paginator((list(table)), 6) # Show 25 contacts per page

        try:
           table = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
           table = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            table = paginator.page(paginator.num_pages)
        return table


#admin advertisement view

def list_all_advertisement(request):
    obj = AdvertisementAdminView()
    data = obj.get_all_jobs()
    return render(request, 'advertisement_admin.html', {'jobs': data})


def edit_job_advertisement(request):

    obj = AdvertisementAdminView(job_id=request.POST['job_id'])
    data = obj.get_job_preview()
    form = company_forms.JobAdvertisementForm(initial={
        'job_title': data.job_title,
        'job_position':data.job_position,
        'job_description':data.job_description,
        'employment':data.employment_id,
        'experience':data.experience_id,
        'category':data.category_id,
        'country':data.country_id,
        'cities':data.cities_id,
        'salary_from':data.salary_from,
        'salary_to':data.salary_to,
        'education':data.degree_level_id,
    })
    html = render_to_string('advertisement_dynamic_edit.html', {'job': form, 'job_value': request.POST['job_id']},
                            context_instance=RequestContext(request))
    return HttpResponse(html)


def edit_job_details(request):
    parameters = parse_qs(request.POST['form_val'])
    resp = {}
    obj = AdvertisementAdminView()
    data = obj.update_job_details(parameters, request.POST['description'], request.POST['job_id'])
    return HttpResponse(json.dumps({'status':True}))

def enable_job(request):
    obj = AdvertisementAdminView(job_id=request.POST['job_id'])
    obj.enable_job()
    return HttpResponse(json.dumps({'status':True}))

def disable_job(request):
    obj = AdvertisementAdminView(job_id=request.POST['job_id'])
    obj.disable_job()
    return HttpResponse(json.dumps({'status':True}))

def reject_job(request):
    obj = AdvertisementAdminView(job_id=request.POST['job_id'])
    obj.reject_job()
    return HttpResponse(json.dumps({'status':True}))



