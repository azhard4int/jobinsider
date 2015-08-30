from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
# Create your models here.

class CategoriesManager(models.Manager):
    def enable_category(self, cat_id):
        if self.filter(id=cat_id).update(category_status=1):
            return True
        else:
            return False

    def disable_category(self, cat_id):
        if self.filter(id=cat_id).update(category_status=0):
            return True
        else:
            return False

    def delete_category(self, cat_id):
        if self.filter(id=cat_id).delete():
            return True
        else:
            return False

    def getinfo(self, cat_id):
        detailsObj = self.filter(id=cat_id)
        if detailsObj:
            return detailsObj
        else:
            return False


class Categories(models.Model):

    directory_path = str(settings.MEDIA_ROOT + "/admin/categories/")


    category_name = models.CharField(
        blank=True,
        max_length=255
    )
    category_status = models.IntegerField(
        blank=True,
        default=1   # set active by default
    )   # For Active/Inactive option from the backend panel

    category_image = models.ImageField(
        upload_to=directory_path,
        default=None,
        blank=True
    )
    file_name  = models.CharField(
        blank=True,
        max_length=255
    )

    objects = CategoriesManager()

    def __unicode__(self):
        return unicode(self.category_name)


class SkillsManager(models.Manager):

    def listall(self, cat_id):
        try:
            data = self.filter(category_id=cat_id).all()
        except ObjectDoesNotExist:
            return False
        print data
        if data:
            return data
        else:
            return False

    def enable_status(self, skill_id):
        try:
            data = self.filter(id=skill_id).update(skill_status=1)
            return True
        except ObjectDoesNotExist:
            return False

    def disable_status(self, skill_id):
        try:
            data = self.filter(id=skill_id).update(skill_status=0)
            return True
        except ObjectDoesNotExist:
            return False

    def delete_status(self, skill_id):
        try:
            data = self.filter(id=skill_id).delete()
            return True
        except ObjectDoesNotExist:
            return False

    def getinfo(self, skill_id):
        detailsObj = self.filter(id=skill_id)
        if detailsObj:
            return detailsObj
        else:
            return False


class Skills(models.Model):
    category = models.ForeignKey(Categories)
    skill_name = models.CharField(
        blank=True,
        max_length=255
    )
    skill_status = models.IntegerField(
        blank=True,
        default=1   # set active by default
    )   # For active/inactive status from the backend

    objects = SkillsManager()

    def __unicode__(self):
        return unicode(self.skill_name)

    # def listall(self, cat_id):
    #     if self.objects



class TimeStamp(models.Model):


    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True