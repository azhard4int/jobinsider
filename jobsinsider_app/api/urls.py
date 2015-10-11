__author__ = 'azhar'
from django.conf.urls import url, include
from django.conf.urls import patterns
from views import *

urlpatterns = patterns(
    url(r'', default, name='api'),
    url(r'^$', default, name='api'),
    url(r'^index/$', default, name='api'),
    url(r'^categories/$', get_categories, name='apiCategories'),
    url(r'^countries/$', get_countries, name='apiCountries'),
    url(r'^cities/(?P<city_id>[0-9]+)$', get_cities, name='apiCities'),
    url(r'^education/$', get_education, name='apiEducation'),
    url(r'^employment/$', get_employment, name='apiEmployment'),
    url(r'^experience/$', get_experience, name='apiExperience'),
    )