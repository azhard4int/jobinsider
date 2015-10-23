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
    list = obj.fetch_filtered_adverts(
        category=request.GET.get('categories'),
        experience=request.GET.get('experience'),
        education=request.GET.get('education'),
        employment=request.GET.get('employment'),

    )
    print list
    page = request.GET.get('page')
    ajax = request.GET.get('is_ajax')
    job_advertisement = obj.paginate_data(list, page)
    return build_template(request,ajax,job_advertisement, filtered_results=1)


class Job_Details(View):
    """
    Detailed job page view
    """
    def get(self, request, job_id):
        data_obj = SearchView()
        data = data_obj.fetch_job_details(job_id)
        is_applied = data_obj.is_already_applied(request.user.id, job_id)
        is_applied_status = False
        if is_applied:
            is_applied_status = True
        is_company = False
        if accounts_models.UserProfile.objects.filter(user_id=request.user.id)[0].user_status == 1:
            is_company = True

        company = data_obj.fetch_company_details(data.company_user_id)
        return render(request, 'jobs_detail.html', {
            'job': data,
            'company':company,
            'user_status':request.user.id,
            'is_applied': is_applied_status,
            'is_company': is_company
        })

    def post(self, request, job_id):
        """
        """
        company_models.AdvertisementApplied(
            user_id = request.user.id,
            advertisement_id = job_id

        ).save()
        return HttpResponse('Job Applying Done Successfully!')

