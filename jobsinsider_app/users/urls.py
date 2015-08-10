__author__ = 'azhar'
from django.conf.urls import url
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(

    url(r'', index),
    url(r'^create-basic-profile/$', index)


)