__author__ = 'azhar'
from django.conf.urls import url
from django.conf.urls import patterns
from views import register, index, login, forgot_password

urlpatterns = patterns(
    url('', index),
    url(r'^register/$', register),
    url(r'^login/$', login),
    url(r'^forgot/$', forgot_password),
    )
