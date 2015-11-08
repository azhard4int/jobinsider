from django.shortcuts import render
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string


# Create your views here.
from django.shortcuts import *
from django.views.generic import View
from datetime import datetime
from models import *
from core import models as core_models
from accounts import models as accounts_models
from company import models as company_models
from users import models as users_models


def build_template(request, ajax,job_advertisement, filtered_results, is_favorite_job=None, is_job_applied=None):
    user_status = None
    obj = SearchView()

    try:
        if request.user.id:
            user_status = obj.is_user_job_seeker(request.user.id)
    except Exception as IndexError:
        user_status = 1
        pass
    if is_favorite_job:
        #if this is the favorite page request
        if ajax == '1':
            html = render_to_string('jobs_view.html', {
                'data':job_advertisement,
                'user_status': user_status,
                'filtered_results': filtered_results
                })
            return HttpResponse(html)
        else:
            return render(request, 'jobs_favorite.html', {
                'data':job_advertisement,
                'user_status': user_status,
                'filtered_results': filtered_results
            })
    elif is_job_applied:
        if ajax == '1':
            html = render_to_string('jobs_view.html', {
                'data':job_advertisement,
                'user_status': user_status,
                'filtered_results': filtered_results
                })
            return HttpResponse(html)
        else:
            return render(request, 'jobs_applied.html', {
                'data':job_advertisement,
                'user_status': user_status,
                'filtered_results': filtered_results
            })
    else:
        if ajax == '1':
            html = render_to_string('jobs_view.html', {
                'data': job_advertisement,
                'user_status': user_status,
                'filtered_results': filtered_results
                })
            return HttpResponse(html)
        else:
            return render(request, 'index.html', {
                'data': job_advertisement,
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


class Favorite_Job(View):
    """
    Favorite Jobs Advertisement List
    """
    def get(self, request):
        """
        """
        obj = SearchView()
        list_all = obj.get_favorite_jobs(request.user.id)
        page = request.GET.get('page')
        ajax = request.GET.get('is_ajax')
        job_advertisement = obj.paginate_data(list_all, page)
        return build_template(request,ajax,job_advertisement, filtered_results=0, is_favorite_job=True)

    def post(self, request):
        """

        :param request:
        :return:
        """

class Applied_Job(View):
    """
    Favorite Jobs Advertisement List
    """
    def get(self, request):
        """
        """
        obj = SearchView()
        list_all = obj.get_applied_jobs(request.user.id)
        page = request.GET.get('page')
        ajax = request.GET.get('is_ajax')
        job_advertisement = obj.paginate_data(list_all, page)
        return build_template(request,ajax,job_advertisement, filtered_results=0, is_job_applied=True)

    def post(self, request):
        """

        :param request:
        :return:
        """


class Job_Details(View):
    """
    Detailed job page view
    """
    def get(self, request, job_id):
        data_obj = SearchView()
        data = data_obj.fetch_job_details(job_id)
        is_applied = data_obj.is_already_applied(request.user.id, job_id)
        is_favorite = data_obj.is_already_favorite(request.user.id, job_id)
        is_favorite_status = False
        is_applied_status = False
        if is_applied:
            is_applied_status = True
        if is_favorite:
            is_favorite_status = True
        is_company = False
        if accounts_models.UserProfile.objects.filter(user_id=request.user.id)[0].user_status == 1:
            is_company = True

        company = data_obj.fetch_company_details(data.company_user_id)
        return render(request, 'jobs_detail.html', {
            'job': data,
            'company':company,
            'user_status':request.user.id,
            'is_applied': is_applied_status,
            'is_company': is_company,
            'is_favorite': is_favorite_status
        })

    def post(self, request, job_id):
        """
        """
        company_models.AdvertisementApplied(
            user_id = request.user.id,
            advertisement_id = job_id

        ).save()
        # increment the value of the job advertisement
        total_count = company_models.Advertisement.admanager.applied_user(job_id)
        company_models.Advertisement.admanager.is_total_applied(job_id, total_count)
        return HttpResponse('Job Applying Done Successfully!')

def add_favorite_job(request):
    data_obj = SearchView()
    company_models.AdvertisementFavorite(
            user_id = request.user.id,
            advertisement_id = request.POST['job_id'],
            add_date = datetime.now()
        ).save()
    return HttpResponse('Job Applying Done Successfully!')

def remove_favorite_job(request):
    data_obj = SearchView()
    company_models.AdvertisementFavorite.objects.filter(
        user_id=request.user.id,
        advertisement_id=request.POST['job_id']).delete()
    return HttpResponse('Job Deleted Successfully!')

