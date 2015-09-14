from django.db import models
from django.contrib.auth.models import User

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

    def __unicode__(self):
        return unicode(self.company_name)

 # - Employee_Size
 # - Headquarters
 # - Industry
 # - Company_Logo
 # - User_Profile_Location (Foreign Key)
