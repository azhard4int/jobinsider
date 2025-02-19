from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from .forms import *
from .models import *
from django.core import serializers
from django.template import context, loader
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger

from evaluation import models as evaluation_model
from core import models as modeinsert
from company import models as company_model

import simplejson as json
from datetime import *
from itertools import chain
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


@login_required()
def users_view(request):
    query = "SELECT * From auth_user JOIN accounts_userprofile on auth_user.id=accounts_userprofile.user_id"
    table =  User.objects.raw(query)
    paginator = Paginator((list(table)), 2) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        table = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        table = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        table = paginator.page(paginator.num_pages)
    return render(request, 'users_view.html',{'table':table})


class User_View(View):
    def get(self,request):
        query = "SELECT * From auth_user JOIN accounts_userprofile on auth_user.id=accounts_userprofile.user_id"
        table =  User.objects.raw(query)
        paginator = Paginator((list(table)), 2) # Show 25 contacts per page
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

        data = User.objects.filter(id=request.POST['id']).update(username=username,first_name=first_name,last_name=last_name,email=email,is_active=int(is_active), is_staff=int(staff),is_superuser=int(superuser))
        #data = User.objects.filter(id=request.POST['id']).update()
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
            except Exception as hello:
                     print hello

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



                 activeusers

@login_required()
def activeusers(request):
         try:
            data=User.objects.filter(is_active=1)
            wholedata = serializers.serialize('json', data)
            if data:
                return HttpResponse(json.dumps({'user_info': wholedata}))
         except Exception as e:
                 print e



@login_required()
def nonactiveusers(request):
         try:
            data=User.objects.filter(is_active=0).order_by('date_joined')
            wholedata = serializers.serialize('json', data)
            if data:
                return HttpResponse(json.dumps({'user_info': wholedata}))
         except Exception as e:
                 print e

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
        return render(request, 'list_education.html', {'edu': eduForm, 'edu_list': list_all})

    def post(self, request):
        modelf.Education(
            education_name=request.POST['education_name']
        ).save()
        return HttpResponse(json.dumps({'status': True}))


def education_delete(request):
    if request.method == 'POST':
        modelf.Education.objects.filter(id=request.POST['education_id']).delete()
        return HttpResponse(json.dumps({'status': True}))


def education_enable(request):
    if request.method == 'POST':
        modelf.Education.objects.filter(id=request.POST['education_id']).update(education_status=1)
        return HttpResponse(json.dumps({'status': True}))


def education_disable(request):
    if request.method == 'POST':
        modelf.Education.objects.filter(id=request.POST['education_id']).update(education_status=0)
        return HttpResponse(json.dumps({'status': True}))


def education_edit(request):
    if request.method == 'POST':
        print request.POST['status']
        if request.POST['status'] == '0':
            edu_id = modelf.Education.objects.filter(id=request.POST['education_id'])[0]
            return HttpResponse(json.dumps({'edu_id':edu_id.education_name}))
        else:
            modelf.Education.objects.filter(id=request.POST['education_id']).update(
                education_name=request.POST['edit_education_name']
            )
            return HttpResponse(json.dumps({'edu_id': True}))


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
            return HttpResponse(json.dumps({'emp_id': emp_id.experience_name}))
        else:
            modelf.Employment.objects.filter(id=request.POST['employment_id']).update(
                employment_name=request.POST['edit_employment_name']
            )
            return HttpResponse(json.dumps({'emp_id':True}))


    try:
       table = evaluation_model.evaluation_test_template.objects.filter(user_id=14)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin_default.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin_default.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))


def evaluation_index(request):
    try:
       table = evaluation_model.evaluation_test_template.objects.filter(evaluation_status=0).exclude(user_id=14)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin.html',{'status':'Falses'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))


def evaluation_default(request):
    try:
       table = evaluation_model.evaluation_test_template.objects.filter(user_id=14)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin_default.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin_default.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def evaluation_user(request):
    try:
       table = evaluation_model.evaluation_test_template.objects.filter(evaluation_status=1).exclude(user_id=14)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin_approved.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin_approved.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def evaluation_user_pending(request):
    try:
       table = evaluation_model.evaluation_test_template.objects.filter(evaluation_status=0).exclude(user_id=14)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))


def evaluation_user_approved(request):
    try:
       table = evaluation_model.evaluation_test_template.objects.filter(evaluation_status=1).exclude(user_id=14)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def evaluation_user_rejected(request):
    try:
       table = evaluation_model.evaluation_test_template.objects.filter(evaluation_status=2).exclude(user_id=14)
       table2 = pagination_table(request.GET.get('page'),table)

       if table and table2:
           return render(request, 'evaluation_index_admin_rejected.html',{'evaluation':table2})
       else:
           return render(request, 'evaluation_index_admin_rejected.html',{'status':'False'})

    except Exception as e:
               return HttpResponse(json.dumps({'status': 'Err'}))

def edit_evaluation_question(request,id):
    try:
         query = evaluation_model.evaluation_test_questions.objects.filter(evaluation_test_template_id=id)
         if query:
            return render(request, 'evaluation_edit_questions_admin.html',{'query':query})

         else:return render(request, 'evaluation_edit_questions_admin.html')


    except Exception as e:
            return render(request, 'evaluation_edit_questions_admin.html')


def addtemplate(request):
    try:
        query = evaluation_model.evaluation_test_template(
            evaluation_name=request.POST['evaluation_name'],
            evaluation_description=request.POST['evaluation_description'],
            evaluation_catagory=request.POST['evaluation_catagory'],
            evaluation_rules=request.POST['evaluation_rules'],
            evaluation_status=1,
            evaluation_type=int(request.POST['evaluation_type']),
            evaluation_total_questions=int(request.POST['evaluation_questions']),
            user_id=14
        )
        query.save()
        obj = evaluation_model.evaluation_test_template.objects.latest('id')
        whole = {
               'evaluation_id': obj.id,
               'evaluation_name': request.POST['evaluation_name'],
               'evaluation_catagory': request.POST['evaluation_catagory'],
               'evaluation_status': 0,
               'evaluation_type': request.POST['evaluation_type'],
               'evaluation_total_questions':request.POST['evaluation_questions']
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
        query = evaluation_model.evaluation_test_template.objects.filter(id=request.POST['id']).update(evaluation_status=1)
        if query:
             return HttpResponse(json.dumps({'status': 'True'}))
        else:
             return HttpResponse(json.dumps({'status': 'False'}))

    except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': 'Err'}))


def reject_evaulation(request):
    try:
        query = evaluation_model.evaluation_test_template.objects.filter(id=request.POST['id']).update(evaluation_status=2)

        if query:
             return HttpResponse(json.dumps({'status': 'True'}))
        else:
             return HttpResponse(json.dumps({'status': 'False'}))

    except Exception as e:
            print e
            return HttpResponse(json.dumps({'status': 'Err'}))


def edit_user_template_by_admin(request):
         try:

             query = evaluation_model.evaluation_test_template.objects.filter(id=request.GET['id'])
             list= {
                 'id':query[0].id,
                 'evaluation_name':query[0].evaluation_name,
                 'evaluation_description':query[0].evaluation_description,
                 'evaluation_rules':query[0].evaluation_rules,
                 'evaluation_catagory':query[0].evaluation_catagory,
                 'evaluation_type':query[0].evaluation_type,
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