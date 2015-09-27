__author__ = 'azhar'
from django.conf.urls import url, include
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(
    url(r'', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^index/$', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^posted-jobs/$', Posted_jobs.as_view(), name='posted_jobs'),
    url(r'^messages/$', Messages.as_view(), name='posted_jobs'),
    url(r'^list/$', CompanyListing.as_view(), name='company_list'),
    url(r'^changepassword/$', CompanyPassword.as_view(), name='company_password'),
    url(r'^profile/$', CompanyProfileView.as_view(), name='company_profile'),
    url(r'^create-job/$', CompanyJobAd.as_view(), name='job_advertisement'),
    url(r'^settings-job/(?P<last_id>[0-9]+)$', CompanyAdSettings.as_view(), name='job_settings'),
    url(r'^finalize-job/$', CompanyJobAdFinalize.as_view(), name='job_finalize'),

    # url(r'^tinymce/', include('tinymce.urls')),

    # url(r'^messages/$', Messages.as_view(), name='posted_jobs'),
    # url(r'^messages/$', Messages.as_view(), name='posted_jobs'),

    )