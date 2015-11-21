from django.db import models
from django.contrib.auth.models import User

from core import models as core_models
from users import models as users_models

# Create your models here.
class CompanyProfileManager(models.Manager):
    """
    Company profile manager include basic set functions
    """

class CompanyProfile(models.Model):
    """
    Basic company model information
    """
    user = models.ForeignKey(User)
    company_name = models.CharField(
        default=None,
        blank=True,
        max_length=255
    )
    your_role = models.CharField(
        default=None,
        blank=True,
        max_length=255
    )
    company_intro  = models.TextField(
        default=None,
        blank=True
    )
    company_url = models.URLField(
        default=None,
        blank=True
    )
    company_industry = models.CharField(
        default=None,
        blank=True,
        max_length=255
    )
    company_status = models.BooleanField(
        default=1
    )
    def __unicode__(self):
        return unicode(self.company_name)

 # - Employee_Size
 # - Headquarters
 # - Industry
 # - User_Profile_Location (Foreign Key)

 # - Company_Logo


class Experience(models.Model):
    experience_name = models.CharField(
        default=None,
        max_length=255,
        blank=True
    )
    experience_status = models.BooleanField(
        blank=True,
        default=1
    )

    def __unicode__(self):
        return (self.experience_name)


class Employment(models.Model):
    employment_name = models.CharField(
        default=None,
        max_length=255,
        blank=True
    )
    employment_status = models.BooleanField(
        blank=True,
        default=1
    )

    def __unicode__(self):
        return (self.employment_name)

class AdvertisementManager(models.Manager):
    def posted(self, user_id):
        return super(AdvertisementManager, self).get_queryset().filter(company_user_id=user_id).prefetch_related(
            'category'
        ).prefetch_related(
            'country'
        ).prefetch_related('cities').order_by('-submission_date')

    def applied_user(self, job_id):
        return super(AdvertisementManager, self).get_queryset().filter(id=job_id)[0].total_applied

    def is_total_applied(self, job_id, current_count):
        current_count = current_count + 1
        return super(AdvertisementManager, self).get_queryset().filter(id=job_id).update(
            total_applied = current_count
        )


class Advertisement(models.Model):
    job_title = models.CharField(
        default=None,
        max_length=255,
        blank=True
    )
    job_position = models.IntegerField(
        default=1,
        blank=True
    )
    job_description = models.TextField(
        blank=True
    )
    company_user = models.ForeignKey(User, default=None)
    company = models.CharField(default=None, max_length=255)
    experience = models.ForeignKey(Experience)
    employment = models.ForeignKey(Employment)
    category = models.ForeignKey(core_models.Categories)
    country = models.ForeignKey(core_models.Countries)
    cities = models.ForeignKey(core_models.Cities)
    salary_from = models.BigIntegerField(
        default=10000
    )
    salary_to = models.BigIntegerField(
        default=10000
    )
    degree_level = models.ForeignKey(core_models.Education)
    submission_date = models.DateTimeField(
        default=None,
        blank=True
    )
    approval_date =  models.DateTimeField(
        default=None,
        blank=True,
        null=True

    )
    job_approval_status = models.PositiveIntegerField(
        default=0,

    )
    job_note_user = models.CharField(
        default=None,
        max_length=255,
        blank=True,
        null=True
    )
    is_draft = models.BooleanField(
        default=False,
    )
    total_applied = models.IntegerField(
        default=0
    )
    admanager = AdvertisementManager()

    def __unicode__(self):
        return unicode(self.job_title)

class AdvertisementApplied(models.Model):
    """Applied people links"""
    advertisement = models.ForeignKey(Advertisement, default=None)
    user = models.ForeignKey(User, default=None)
    # location = models.ForeignKey(users_models.UserLocation, default=None)
    is_shortlisted = models.BooleanField(default=False)
    applied_date = models.DateTimeField(default=None)

    def __unicode__(self):
        return unicode(self.advertisement)

class ShortlistedCandidates(models.Model):
    advertisement = models.ForeignKey(Advertisement, default=None)
    user = models.ForeignKey(User, default=None)
    shortlisted_date = models.DateTimeField(default=None)

    def __unicode__(self):
        return unicode(self.advertisement)


class AdvertisementFavorite(models.Model):
    """
    I have to add the models here base don the user criteria
    """
    advertisement = models.ForeignKey(Advertisement, default=None)
    user = models.ForeignKey(User, default=None)
    add_date = models.DateTimeField(default=None)

    def __unicode__(self):
        return unicode(self.advertisement)

class AdvertisementSettings(models.Model):
    """
    Basic checks for advertisement settings.
    """
    is_email = models.BooleanField(
        default=False
    )
    is_map_show = models.BooleanField(
        default=False
    )
    apply_date = models.DateField(
        default=None,
        blank=True,
        null=True

    )
    is_apply_true = models.BooleanField(
        default=False
    )
    advertisement = models.OneToOneField(Advertisement, default=None)


class AdvertisementAnalytics(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    user_agent = models.CharField(
        default=None,
        max_length=255
    )
    user_agent_family = models.CharField(
        default=None,
        max_length=255
    )
    user_agent_version = models.CharField(
        default=None,
        max_length=255
    )
    remote_address = models.CharField(
        default=None,
        max_length=255
    )
    os_family = models.CharField(
        default=None,
        max_length=255
    )
    os_version = models.CharField(
        default=None,
        max_length=255
    )
    total_visitors = models.CharField(
        default=None,
        max_length=255
    )
    unique_visitors = models.CharField(
        default=None,
        max_length=255
    )

    #Gender: 0 for male and 1 for female
    is_gender = models.IntegerField(
        default=0,
    )
    post_date = models.DateField(
        default=None,
    )
    country_short = models.CharField(
        default=None,
        max_length=255
    )
    country_long = models.CharField(
        default=None,
        max_length=255
    )
    visitor_gender = models.IntegerField(
        default=2,
    )

    def __unicode__(self):
        return unicode(self.advertisement)



