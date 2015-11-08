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

    def toCheck(self, object_name, object):
        """
        Splitting the values and returning data
        """
        if not object_name:
            data =[]
            for data_value in object:
                data.append(data_value.id)
        else:
            data= object_name.split(',')
        return data

    def fetch_filtered_adverts(self, category=None, employment=None, experience=None, education=None):
        """
        Retrieves only filtered results
        """
        allCategories = core_models.Categories.objects.all()
        allEducation = core_models.Education.objects.all()
        allExperience = company_models.Experience.objects.all()
        allEmployment = company_models.Employment.objects.all()
        category = self.toCheck(category, allCategories)
        experience = self.toCheck(experience, allExperience)
        employment = self.toCheck(employment, allEmployment)
        education = self.toCheck(education, allEducation)
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
        ).filter(
            experience__in=experience,
            category__in=category,
            degree_level__in=education,
            employment__in=employment,
            job_approval_status=1
        ).order_by('-submission_date')
        return data


    def fetch_job_details(self, job_id):
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
        ).filter(
            id=job_id
        )[0]
        return data

    def fetch_company_details(self, user_id):
        data = company_models.CompanyProfile.objects.filter(user_id=user_id)[0]
        return data

    def is_already_applied(self, user_id,job_id):
        try:
            data = company_models.AdvertisementApplied.objects.filter(user_id=user_id, advertisement_id=job_id)[0]
            if data:
                return True
        except IndexError:
            return False

    def is_already_favorite(self, user_id,job_id):
        try:
            data = company_models.AdvertisementFavorite.objects.filter(user_id=user_id, advertisement_id=job_id)[0]
            if data:
                return True
        except IndexError:
            return False

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

    def get_favorite_jobs(self, user_id):
        data = company_models.AdvertisementFavorite.objects.filter(user_id=user_id)
        advertisement_id = []
        if data:
            for ab in data:
                advertisement_id.append(ab.advertisement_id)
        whole_data = company_models.Advertisement.admanager.prefetch_related(
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
            job_approval_status=1,
            id__in=advertisement_id
        ).order_by('-submission_date')
        print whole_data
        return whole_data

    def get_applied_jobs(self, user_id):
        data = company_models.AdvertisementApplied.objects.filter(user_id=user_id)
        advertisement_id = []
        if data:
            for ab in data:
                advertisement_id.append(ab.advertisement_id)
        whole_data = company_models.Advertisement.admanager.prefetch_related(
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
            job_approval_status=1,
            id__in=advertisement_id
        ).order_by('-submission_date')
        print whole_data
        return whole_data