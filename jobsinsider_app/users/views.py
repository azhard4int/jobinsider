from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Status: Welcome to Basic Profile')