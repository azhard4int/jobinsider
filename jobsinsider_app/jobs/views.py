from django.shortcuts import render

# Create your views here.
from django.shortcuts import *
from django.views.generic import View


class Default_Search(View):
    def get(self, request):
        return HttpResponse('Hello Wrold')