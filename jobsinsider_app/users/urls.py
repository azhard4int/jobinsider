__author__ = 'azhar'
from django.conf.urls import url
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(

    url(r'', index),
    url(r'^create-basic-profile/$', index),
    url(r'^dashboard/$', UserDashboard.as_view()),
    url(r'^skills_list/$', skills_list),
    url(r'^skills/$', skills),
    url(r'^cities/$', cities),
    url(r'^profile_bio/$', UserInfo.as_view()),
    url(r'^profile_cv/$', UserCVUpload.as_view()),
    url(r'^add_user_employment/$', AddCVEmployment),
    url(r'^add_employment/$', AddUserEmployment.as_view()),
    url(r'^remove_employment/(?P<emp_id>[0-9]+)/$', remove_employment, name='remove_employment'),
    url(r'^remove_education/(?P<edu_id>[0-9]+)/$', remove_education, name='remove_education'),
    url(r'^complete_profile/$', complete_profile, name='complete_profile'),
    url(r'^is_cv_builder/$', is_cv_builder, name='is_cv_builder'),
    url(r'^education/$', EducationUpdate.as_view()),
    url(r'^u/$', Profile.as_view(), name='user_profile'),     # (?P<username>[A-Za-z0-9]+)/
    url(r'^u/changepassword/$', ProfileChangePassword.as_view(), name='user_change_password'),
    url(r'^u/profile/$', ProfileUser.as_view(), name='profile'),
    url(r'^u/profile_settings/$', ProfileSettings.as_view(), name='profile_settings'),
    url(r'^u/profile_settings/education/$', ProfileSettingsEducation.as_view(), name='profile_settings_education'),
    url(r'^u/profile_settings/education/edit/$', edit_education_description, name='edit_education_description'),
    url(r'^u/profile_settings/education/delete/$', delete_education_description, name='delete_education_description'),
    url(r'^u/profile_settings/employment/$', ProfileSettingsEmployment.as_view(), name='profile_settings_employment'),
    url(r'^u/profile_settings/employment/edit/$', edit_company_description, name='edit_company_description'),
    url(r'^u/profile_settings/employment/delete/$', delete_company_description, name='delete_company_description'),
    url(r'^u/profile_settings/resume/$', ProfileSettingsResume.as_view(), name='profile_resume'),
    url(r'^messages/$', UserMessages.as_view(), name='user_messages'),
    url(r'^job_alert/$', JobAlertView.as_view(), name='job_alert')
)