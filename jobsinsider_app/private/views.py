from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from core import models as modeinsert
import simplejson as json



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

    if request.method=='POST':
        category_status = request.POST['category_status']
        category_name = request.POST['category_name']
        catInstance = modeinsert.Categories(
            category_status=category_status,
            category_name=category_name
        )
        catInstance.save()

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
def skills_view(request):
    """

    :param request:
    :return:
    """


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

def skill_view_delete(request):
    '''

    :param request:
    :return:
    '''

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('http://127.0.0.1:8000/accounts/login/')