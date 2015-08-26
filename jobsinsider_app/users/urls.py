__author__ = 'azhar'
from django.conf.urls import url
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(

    url(r'', index),
    url(r'^create-basic-profile/$', index),
    url(r'^skills_list/$', skills_list),
    url(r'^skills/$', skills),
    url(r'^profile_bio/$', UserInfo.as_view()),
    url(r'^profile_cv/$', UserCVUpload.as_view()),
    url(r'^add_user_employment/$', AddCVEmployment),
    url(r'^add_employment/$', AddUserEmployment.as_view()),
)