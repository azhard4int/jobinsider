from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from .forms import Adminlogin
from .models import UsersAccounts


# Create your views here.
def index(request):
    return HttpResponse('Logged in as Administrator')


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


def members_view(request):
    """
    For administrator based users to show them the data
    """
    user = UsersAccounts()
    user_accounts = user.list_all()
    return render(request, 'list.html', {'listusers': user_accounts})

def categories_view(request):
    """

    :param request:
    :return:
    """

def skills_view(request):
    """

    :param request:
    :return:
    """