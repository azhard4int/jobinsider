from django.db import models

# Create your models here.


class Categories(models.Model):

    category_name = models.CharField(
        blank=True,
        max_length=255
    )
    category_status = models.IntegerField(
        blank=True,
    )   # For Active/Inactive option from the backend panel

    def __unicode__(self):
        return unicode(self.category_name)

class Skills(models.Model):
    category = models.OneToOneField(Categories)
    skill_name = models.CharField(
        blank=True,
        max_length=255
    )
    skill_status = models.IntegerField(
        blank=True
    )   # For active/inactive status from the backend

    def __unicode__(self):
        return unicode(self.skill_name)


class TimeStamp(models.Model):


    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True