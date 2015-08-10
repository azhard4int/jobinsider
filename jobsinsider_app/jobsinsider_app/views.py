__author__ = 'azhar'
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'homepage.html')

@login_required(login_url='/accounts/login/')
def dashboard(request):

    return render(request, 'dashboard.html')
