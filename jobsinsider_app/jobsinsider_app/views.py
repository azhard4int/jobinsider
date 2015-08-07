__author__ = 'azhar'
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')