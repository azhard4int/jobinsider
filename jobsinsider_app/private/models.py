from django.db import models

# Create your models here.

class Admin(models.Model):
    admin_username = models.CharField(
        blank=True,
        max_length=255
    )
