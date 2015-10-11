from django.shortcuts import *
from django.core import serializers

from core import models as coreModels
from accounts import models as accountsModels
from company import models as companyModels




import simplejson as json
# Create your views here.


def default(request):
    status = {
        'status': 'Invalid Request'
    }
    return HttpResponse(json.dumps(status))


def get_categories(request):
    list_all = coreModels.Categories.objects.all()
    list_categories = serializers.serialize('json', list_all)

    return HttpResponse(list_categories)


def get_countries(request):
    list_all = coreModels.Countries.objects.all()
    list_countries = serializers.serialize('json', list_all)

    return HttpResponse(list_countries)


def get_cities(request, city_id=None):
    """
    Fetch cities based on the ID
    """
    if request.method == 'POST':
        list = coreModels.Cities.objects.filter(country_id=city_id).all().order_by('city_name')
        cities = [ab.city_name for ab in list]
        cities_list = serializers.serialize('json', list)
        # for ab in list:
        #     ab.city_name
        return HttpResponse(cities_list)
    else:
        raise Http404


def get_education(request):
    list_all = coreModels.Education.objects.all()
    list_education= serializers.serialize('json', list_all)
    return HttpResponse(list_education)


def get_experience(request):
    list_all = companyModels.Experience.objects.filter(experience_status=1).all()
    list_experience= serializers.serialize('json', list_all)
    return HttpResponse(list_experience)

def get_employment(request):
    list_all = companyModels.Employment.objects.all()
    list_employment= serializers.serialize('json', list_all)
    return HttpResponse(list_employment)