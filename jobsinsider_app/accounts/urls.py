__author__ = 'azhar'
from django.conf.urls import url
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(
    url(r'', index),
    url(r'^register/$', register, name='register_account'),
    url(r'^login/$', login_view, name='login_account'),
    url(r'^forgot/$', forgot_password, name='forgot_password'),
    url(r'^forgot/newpassword$', set_new_password), # for setting up password on token
    url(r'^signup/verify-email/$', confirm_email),  # for verifying token
    url(r'^logout/$', logout_view),  # for verifying token
    )