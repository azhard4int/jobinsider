from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):


    user = models.OneToOneField(User)
    user_status = models.IntegerField(default=0)    # This is for the company/job seeker user.
    user_cv_status = models.BooleanField(default=0)
    user_account_review = models.IntegerField(default=0)    #0 for not approved, 1 approved, 2 rejected.
    user_post_job = models.BooleanField(default=0)  # 0 - no, 1 - yes.
    company_profile_status = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.user)

class UserForgot(models.Model):

    user = models.OneToOneField(User)
    token_key = models.CharField(default=None, max_length=100)
    timestamp = models.DateTimeField(default='0000-00-00 00:00:00')
    token_status = models.BooleanField(default=0)

    def __unicode__(self):
        return unicode(self.user)

class UserActivation(models.Model):


    user = models.OneToOneField(User)
    activation_key = models.CharField(default=None, max_length=100)
    timestamp = models.DateTimeField(default='0000-00-00 00:00:00')
    activation_status = models.BooleanField(default=0)

    def __unicode__(self):
        return unicode(self.user)


