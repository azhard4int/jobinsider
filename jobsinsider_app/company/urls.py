__author__ = 'azhar'
from django.conf.urls import url, include
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(
    url(r'', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^$', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^index/$', Company_dashboard.as_view(), name='company_dashboard'),
    url(r'^posted-jobs/$', Posted_jobs.as_view(), name='posted_jobs'),
    url(r'^messages/$', MessagesView.as_view(), name='messages'),
    url(r'^list/$', CompanyListing.as_view(), name='company_list'),
    url(r'^changepassword/$', CompanyPassword.as_view(), name='company_password'),
    url(r'^profile/$', CompanyProfileView.as_view(), name='company_profile'),
    url(r'^create-job/$', CompanyJobAd.as_view(), name='job_advertisement'),
    url(r'^create-job/evaluation/$', CompanyEvaluation.as_view(), name='company_evaluation'),
    url(r'^job/edit/(?P<job_id>[0-9]+)$$', CompanyAdEdit.as_view(), name='job_advertisement_edit'),
    url(r'^settings-job/(?P<last_id>[0-9]+)$', CompanyAdSettings.as_view(), name='job_settings'),
    url(r'^finalize-job/$', CompanyJobAdFinalize.as_view(), name='job_finalize'),
    url(r'^delete-job/(?P<job_id>[0-9]+)/$', delete_job, name='job_delete'),
    url(r'^pause-job/(?P<job_id>[0-9]+)/$', pause_job, name='job_pause'),
    url(r'^analytics/(?P<job_id>[0-9]+)/$', analytics, name='analytics_view'),
    url(r'^candidates/(?P<job_id>[0-9]+)/$', AppliedCandidates.as_view(), name='applied_candidates'),
    url(r'^candidates/applied/$',applied_country , name='applied_candidates'),
    url(r'^candidates/applied_gender/$',applied_gender, name='applied_gender_candidates'),
    url(r'^candidates/applied_city/$',applied_city, name='applied_city_candidates'),
    url(r'^candidate/(?P<candidate_id>[0-9]+)/$', Candidate.as_view(), name='candidate'),
    url(r'^pdf/(?P<candidate_id>[0-9]+)/$', pdf_render, name='pdf_render'),
    url(r'^shortlisted_candidates/(?P<job_id>[0-9]+)/$', ListShortlisted.as_view(), name='shortlisted_candidates'),
    url(r'^schedule_interview/(?P<candidate_id>[0-9]+)/(?P<job_id>[0-9]+)/$', ScheduleInterview.as_view(), name='schedule_interview'),
    url(r'^shortlist/(?P<candidate_id>[0-9]+)/(?P<job_id>[0-9]+)/$', Shortlisted.as_view(), name='shortlisted'),
    url(r'^shortlist_remove/(?P<candidate_id>[0-9]+)/(?P<job_id>[0-9]+)/$', shortlist_remove, name='shortlisted_remove'),
    url(r'^candidate_remove/(?P<candidate_id>[0-9]+)/(?P<job_id>[0-9]+)/$', candidate_remove, name='candidate_remove'),
    url(r'^message/$', SendMessage.as_view(), name='send_message'),
    url(r'^composedmessage/$', ComposedSend.as_view(), name='composed_message'),
    url(r'^shortlisted_candidates_date/$', ShortlistedCandidatesDate.as_view(), name='composed_message'),
    url(r'^candidates/all/$', CompanyAppliedAll.as_view(), name='applied_candidates_all'),
    url(r'^shortlist/all/$', CompanyShortlistedAll.as_view(), name='shortlisted_candidates_all'),
    url(r'^message/notification/$', Message_nofication.as_view(), name='Get-message-notification'),
    url(r'^message/notification/admin-notify/$', Admin_notify.as_view(), name='Get-admin-message-notification'),
    url(r'^message/notification/get-admin-notify/$', Get_notify.as_view(), name='Get-admin-notification')


    # url(r'^tinymce/', include('tinymce.urls')),

    # url(r'^messages/$', Messages.as_view(), name='posted_jobs'),
    # url(r'^messages/$', Messages.as_view(), name='posted_jobs'),

    )