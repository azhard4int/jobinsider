from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from .forms import Adminlogin

# Create your views here.
def index(request):
    return HttpResponse('Logged in as Administrator')


def login_admin_view(request):
    """
    Only for the administrator privilleged users.
    """
    admin = Adminlogin()
    return render(request, 'admin_login.html', {'admin_form': admin})


def members_view(request):
    """
    For administrator based users to show them the data
    """