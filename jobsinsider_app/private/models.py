from django.db import models
from django.contrib.auth.models import User
from core import models as modelcore

# Create your models here.
class UsersAccounts:


    def list_all(self):
        user = User.objects.all()
        return user


class CategoriesInstance:

    def list_all(self):
        return modelcore.Categories.objects.all()

    def count_items(self):
        return modelcore.Categories.objects.count()

    def edit_item(self, edit_id):
        """

        :param edit_id:
        :return:
        """

