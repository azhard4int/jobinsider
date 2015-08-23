import simplejson as json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers

from models import *



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
            cats = list_categories.list_categories()
            return render(request, 'user_selection.html', {'categories':cats})

        if step_value == '1':
            return render(request, 'cv_selection_page.html')

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
