from django.db import models

# Create your models here.
class TimeStamp(models.Model):


    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True

"""
class Categories(models.Model):

    category_name = models.CharField(blank=True)

    def __unicode__(self):
        return self.category_name

    # def add_category(self, category):

class

"""