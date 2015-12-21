__author__ = 'azhar'
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from .forms import *
from .models import *
from django.db import models
from django.core import serializers
from django.template import context, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urlparse import urlparse, parse_qs


from evaluation import models as evaluation_models
from core import models as core_models
from company import models as company_models

from django.db import models
from accounts import models as accounts_models
from users import models as user_models
from django.db.models.query import RawQuerySet

import simplejson as json
from datetime import *
import time


class AdvertisementAdminView(object):

    def __init__(self, user_id=None, keyword=None, from_date=None, to_date=None, job_id=None):
        self.user_id=user_id
        self.keyword=keyword
        self.to_date=to_date
        self.from_date=None
        self.job_id=job_id

    def get_all_jobs(self):
        return company_models.Advertisement.admanager.all().order_by('-submission_date')

    def get_all_jobs_id(self):
        return company_models.Advertisement.admanager.filter(user_id=self.user_id).order_by('-submission_date')

    def get_all_approved(self):
        return company_models.Advertisement.admanager.filter(job_approval_status=1).order_by('-submission_date')

    def get_all_pending(self):
        return company_models.Advertisement.admanager.filter(job_approval_status=0).order_by('-submission_date')

    def get_all_rejected(self):
        return company_models.Advertisement.admanager.filter(job_approval_status=2).order_by('-submission_date')

    def get_all_rejected_id(self):
        return company_models.Advertisement.admanager.filter(job_approval_status=2, user_id=self.user_id).order_by('-submission_date')

    def get_all_pending_id(self):
        return company_models.Advertisement.admanager.filter(job_approval_status=0, user_id=self.user_id).order_by('-submission_date')

    def get_all_approved_id(self):
        return company_models.Advertisement.admanager.filter(job_approval_status=1, user_id=self.user_id).order_by('-submission_date')

    def get_all_jobs_date(self):
        return company_models.Advertisement.admanager.filter(submission_date__gt=self.from_date,
                                                                     submission_date__lt=self.to_date).order_by('-submission_date')

    def get_job_preview(self):
        return company_models.Advertisement.admanager.filter(id=self.job_id)[0]

    def update_job_details(self, parameters, description, job_id=None):
        company_models.Advertisement.admanager.filter(id=parameters['job_id'][0]).update(
                    job_title=parameters['job_title'][0],
                    job_position=parameters['job_position'][0],
                    job_description=description,
                    employment_id=parameters['employment'][0],
                    experience_id=parameters['experience'][0],
                    category_id=parameters['category'][0],
                    salary_from=parameters['salary_from'][0],
                    salary_to=parameters['salary_to'][0],
                    degree_level_id=parameters['education'][0],
                    is_evaluation_test=False
                    # submission_date=datetime.now(),
                    )

    def enable_job(self):
        company_models.Advertisement.admanager.filter(id=self.job_id).update(
            job_approval_status=1
        )

    def disable_job(self):
        company_models.Advertisement.admanager.filter(id=self.job_id).update(
            job_approval_status=0
        )

    def reject_job(self):
        company_models.Advertisement.admanager.filter(id=self.job_id).update(
            job_approval_status=2
        )