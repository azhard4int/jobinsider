__author__ = 'azhar'
from django.conf.urls import patterns
from django.conf.urls import url
from views import *

urlpatterns = patterns(
    url(r'', index),
    url(r'^login/$', login_admin_view),
    url(r'^members/$', members_view),
    url(r'^members/categories/$', categories_view, name='cat_view'),
    url(r'^members/categories/skills', skills_view),
    url(r'^members/logout', logout_view),
    url(r'^members/categories/add_category', process_catadd),   #this is for adding categories
    url(r'^members/categories/enable/', process_enable_status),
    url(r'^members/categories/disable/', process_disable_status),
    url(r'^members/categories/delete/', process_delete_status),
    url(r'^members/categories/edit/(?P<editid>[0-9]+)/$', process_edit_form),
    url(r'^members/categories/editcategory/$', process_category_edit),
    url(r'^members/categories/skill_enable/$', skill_view_enable),
    url(r'^members/categories/skill_disable/$', skill_view_disable),
    url(r'^members/categories/skill_delete/$', skill_view_delete),
)