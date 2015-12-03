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
    url(r'^messages/$', UserMessages.as_view(), name='user_messages')


)