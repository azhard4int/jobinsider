from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from core import models as core_models
from accounts import models as accounts_models
from company import models as company_models
from users import models as users_models
# Create your models here.


class SearchView():

    def fetch_all_adverts(self):
        data = company_models.Advertisement.admanager.prefetch_related(
            'category'
        ).prefetch_related(
            'country'
        ).prefetch_related(
            'employment'
        ).prefetch_related(
            'experience'
        ).prefetch_related(
            'degree_level'
        ).prefetch_related(
            'company_user'
        ).prefetch_related(
            'cities'
        ).filter(job_approval_status=1).order_by('-submission_date')
        return data

    def fetch_filtered_adverts(self, category=None, employment=None, experience=None, education=None):
        """
        Retrieves only filtered results
        """
        print category
        data = data = company_models.Advertisement.admanager.prefetch_related(
            'category'
        ).prefetch_related(
            'country'
        ).prefetch_related(
            'employment'
        ).prefetch_related(
            'experience'
        ).prefetch_related(
            'degree_level'
        ).prefetch_related(
            'company_user'
        ).prefetch_related(
            'cities'
        ).filter(
            category__in=category
        ).filter(
            job_approval_status=1
        ).order_by('-submission_date')
        return data

    def is_user_job_seeker(self, id):
        data = accounts_models.UserProfile.objects.filter(user_id=id)[0]
        return data.user_status

    def paginate_data(self, data, page):
        paginator = Paginator(data, 1)
        try:
            jobs_advertisement = paginator.page(page)
        except PageNotAnInteger:
            jobs_advertisement = paginator.page(1)
        except EmptyPage:
            jobs_advertisement = paginator.page(paginator.num_pages)

        return jobs_advertisement