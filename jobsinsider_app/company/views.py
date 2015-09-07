from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.

@login_required()
def index(request):
    return HttpResponseRedirect('/company/')

class Company_dashboard(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'company_dashboard.html')

class Posted_jobs(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'posted_jobs.html')

class Messages(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'company_message.html')