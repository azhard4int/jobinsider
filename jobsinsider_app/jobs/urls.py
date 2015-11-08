__author__ = 'azhar'
from django.conf.urls import url, include
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(
    url(r'', Default_Search.as_view(), name='search'),
    url(r'^index/$', Default_Search.as_view(), name='search'),
    url(r'^filtered/$', filtered_results, name='filtered'),
    url(r'^detail/(?P<job_id>\d+)/$', Job_Details.as_view(), name='job_details'),
    url(r'^add_favorite_job/$', add_favorite_job, name='favorite_job'),
    url(r'^remove_favorite_job/$', remove_favorite_job, name='remove_favorite_job'),
    url(r'^favorite/$', Favorite_Job.as_view(), name='favorite'),
    url(r'^applied/$', Applied_Job.as_view(), name='applied'),
    )