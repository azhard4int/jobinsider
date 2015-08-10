__author__ = 'azhar'
from django.conf.urls import patterns
from django.conf.urls import url
from views import *

urlpatterns = patterns(
    url(r'', index)
)