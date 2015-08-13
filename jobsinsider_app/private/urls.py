__author__ = 'azhar'
from django.conf.urls import patterns
from django.conf.urls import url
from views import *

urlpatterns = patterns(
    url(r'', index),
    url(r'^login/$', login_admin_view),
    url(r'^members/$', members_view),
    url(r'^members/categories/$', categories_view),
    url(r'^members/categories/skills', skills_view)
)