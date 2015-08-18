from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .forms import Adminlogin
from .models import UsersAccounts


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
@login_required()

def categories_view(request):
    """

    :param request:
    :return:
    """

@login_required()
def skills_view(request):
    """

    :param request:
    :return:
    """