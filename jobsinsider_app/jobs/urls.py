__author__ = 'azhar'
from django.conf.urls import url, include
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(
    url(r'', Default_Search.as_view(), name='search'),
    url(r'^index/$', Default_Search.as_view(), name='search'),
    url(r'^filtered/$', filtered_results, name='filtered'),
    url(r'^detail/(?P<job_id>\d+)/$', Job_Details.as_view(), name='job_details'),
    )