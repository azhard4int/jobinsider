__author__ = 'azhar'
from django.conf.urls import url
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(
    url(r'', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^index/$', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^posted-jobs/$', Posted_jobs.as_view(), name='posted_jobs'),
    url(r'^messages/$', Messages.as_view(), name='posted_jobs'),

    )