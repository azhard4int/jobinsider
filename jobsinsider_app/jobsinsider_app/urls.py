"""jobsinsider_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import sys
BASE_PROJECT = sys.path[0]


# from django.conf.urls.defaults import *
from django.conf.urls import include, url, static
from django.conf import settings
from django.contrib import admin
from views import *


urlpatterns = [
    # url(r'', homepage),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^dashboard/', dashboard),
    url(r'^private/', include('private.urls')),
    # url(r'^ajax-upload/', include('ajax_upload.urls')),

] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
