from django.shortcuts import render
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string


# Create your views here.
from django.shortcuts import *
from django.views.generic import View
from models import *
from core import models as core_models
from accounts import models as accounts_models
from company import models as company_models
from users import models as users_models


def build_template(request, ajax,job_advertisement, filtered_results):
    user_status = None
    obj = SearchView()
    try:
        if request.user.id:
            user_status = obj.is_user_job_seeker(request.user.id)
    except Exception as IndexError:
        user_status = 1
        pass
    if ajax == '1':
        html = render_to_string('jobs_view.html', {
            'data':job_advertisement,
            'user_status': user_status,
            'filtered_results': filtered_results
            })
        return HttpResponse(html)
    else:
        return render(request, 'index.html', {
            'data':job_advertisement,
            'user_status': user_status,
            'filtered_results': filtered_results
        })

class Default_Search(View):
    def get(self, request):
        obj = SearchView()
        list_all = obj.fetch_all_adverts()
        page = request.GET.get('page')
        ajax = request.GET.get('is_ajax')
        job_advertisement = obj.paginate_data(list_all, page)
        return build_template(request,ajax,job_advertisement, filtered_results=0)

#to get filtered based results.
def filtered_results(request):
    """
    """
    obj = SearchView()
    list = obj.fetch_filtered_adverts(category=request.GET.get('categories'))
    print list
    page = request.GET.get('page')
    ajax = request.GET.get('is_ajax')
    job_advertisement = obj.paginate_data(list, page)
    return build_template(request,ajax,job_advertisement, filtered_results=1)