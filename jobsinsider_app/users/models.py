from django.db import models
from accounts import models as accmodels
from core import models as coremodels
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


from datetime import datetime

# Create your models here.

class UserSkillsManager(models.Manager):

    def exist_not(self, user_id):
        print user_id
        try:
            print self.all()
            if self.filter(user_id=user_id):
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

class UserSkills(models.Model):
    user = models.OneToOneField(User)
    category = models.ForeignKey(coremodels.Categories)
    skills = models.CharField(blank=True, max_length=255)   # will be stored comma seperated
    skill_status = models.BooleanField(default=0)   # either 0 or 1, if set it will not show again.

    objects = UserSkillsManager()


    def __unicode__(self):
        return unicode(self.user)

    def list_categories(self):
        """
            display all categories that are in the database.
        """
        return coremodels.Categories.objects.filter(category_status=1).all()

    def get_skills(self, cat_id):
        return coremodels.Skills.objects.filter(category_id=cat_id).all()



class UserBio(models.Model):
    """
    Basic Biography of the job seeker information will be stored
    in this table. Step 1
    """
    directory_path = str(settings.MEDIA_ROOT + "/userprofile/")
    user = models.OneToOneField(User)
    user_title = models.CharField(blank=True, max_length=255)
    user_overview = models.TextField(blank=True)
    user_bio_status = models.BooleanField(default=0)
    user_portrait = models.ImageField(upload_to=directory_path)
    user_portrait_filename = models.CharField(default=None, max_length=255,
                                              blank=True, null=True)
    user_language_pre = models.CharField(default=None, max_length=255)
    user_gender = models.IntegerField(default=None)
    # Professional_Title
    # English Proficiency (It will have select box)


    def __unicode__(self):
        return unicode(self.user)



class UserLocation(models.Model):
    """
    User biography information - includes user related personal details.
    This will be in Step 1.
    """
    user = models.OneToOneField(User)
    user_address = models.TextField(blank=True, max_length=255)
    user_city = models.ForeignKey(coremodels.Cities) #models.CharField(blank=True, max_length=255)
    user_country = models.ForeignKey(coremodels.Countries) #models.CharField(blank=True, max_length=255)
    user_zipcode = models.CharField(blank=True, max_length=255)
    user_phone_no = models.CharField(blank=True, max_length=255)
    user_location_status = models.BooleanField(default=0)

    def __unicode__(self):
        return unicode(self.user)


class UserCV(models.Model):

    """
    Storing User CV Details
    """
    directory_path = str(settings.MEDIA_ROOT + "/users/cv/")
    user = models.OneToOneField(User)
    user_cv_title = models.CharField(
        blank=True,
        max_length=255,
        default=None
    )
    user_cv_file = models.FileField(
        upload_to=directory_path + '%Y/%m/%d',
        default=None
    )
    user_cv_builder_status = models.BooleanField(default=0)     # 0 means no to cv builder, 1 means yes.
    user_cv_review_status = models.IntegerField(default=0)  # 0 pending, 1 approved, 2 rejected.
    user_cv_builder = models.IntegerField(default=0)  # 0 pending, 1 approved, 2 rejected.
    user_cv_emp_status = models.BooleanField(default=0)
    user_cv_education = models.IntegerField(default=0)
    def __unicode__(self):
        return unicode(self.user)


class UserEmployment(models.Model):
    """
    Employment table and this will have user previous biodata where
    he worked out. Step 2
    """
    user = models.ForeignKey(User)
    company_name = models.CharField(blank=True, max_length=255)
    company_location = models.CharField(blank=True, max_length=255)
    company_worktitle = models.CharField(blank=True, max_length=255)
    company_role = models.CharField(blank=True, max_length=255)
    company_from = models.DateField(blank=True)
    company_to = models.DateField(blank=True)
    company_description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.user)


class UserEducation(models.Model):
    """
    User previous education field.
    """
    user = models.ForeignKey(User)
    user_institute = models.CharField(
        max_length=255,
        blank=True,
        default=None)
    user_degree = models.CharField(
        max_length=255,
        blank=True,
        default=None)
    degree_from = models.DateField(
        max_length=255,
        blank=True,
        default=None
    )
    degree_to = models.DateField(
        max_length=255,
        blank=True,
        default=None
    )


class JobAlert(models.Model):
    user = models.ForeignKey(User)
    is_status = models.BooleanField(default=True,blank=True)
    category = models.ForeignKey(coremodels.Categories)
    added_date = models.DateTimeField(default=datetime.now(), null=True)

    def __unicode__(self):
        return unicode(self.user)