from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsersAccounts:


    def list_all(self):
        user = User.objects.all()
        return user
