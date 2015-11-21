__author__ = 'azhar'
from django.conf.urls import url, include
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(
    url(r'', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^$', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^index/$', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^posted-jobs/$', Posted_jobs.as_view(), name='posted_jobs'),
    url(r'^messages/$', Messages.as_view(), name='messages'),
    url(r'^list/$', CompanyListing.as_view(), name='company_list'),
    url(r'^changepassword/$', CompanyPassword.as_view(), name='company_password'),
    url(r'^profile/$', CompanyProfileView.as_view(), name='company_profile'),
    url(r'^create-job/$', CompanyJobAd.as_view(), name='job_advertisement'),
    url(r'^job/edit/(?P<job_id>[0-9]+)$$', CompanyAdEdit.as_view(), name='job_advertisement_edit'),
    url(r'^settings-job/(?P<last_id>[0-9]+)$', CompanyAdSettings.as_view(), name='job_settings'),
    url(r'^finalize-job/$', CompanyJobAdFinalize.as_view(), name='job_finalize'),
    url(r'^delete-job/(?P<job_id>[0-9]+)/$', delete_job, name='job_delete'),
    url(r'^analytics/(?P<job_id>[0-9]+)/$', analytics, name='analytics_view'),
    url(r'^candidates/(?P<job_id>[0-9]+)/$', AppliedCandidates.as_view(), name='applied_candidates'),
    url(r'^candidate/(?P<candidate_id>[0-9]+)/$', Candidate.as_view(), name='candidate'),
    url(r'^pdf/(?P<candidate_id>[0-9]+)/$', pdf_render, name='pdf_render'),
    url(r'^shortlist/(?P<candidate_id>[0-9]+)/(?P<job_id>[0-9]+)/$', Shortlisted.as_view(), name='shortlisted'),
    url(r'^shortlist_remove/(?P<candidate_id>[0-9]+)/(?P<job_id>[0-9]+)/$', shortlist_remove, name='shortlisted_remove'),
    # url(r'^tinymce/', include('tinymce.urls')),

    # url(r'^messages/$', Messages.as_view(), name='posted_jobs'),
    # url(r'^messages/$', Messages.as_view(), name='posted_jobs'),

    )