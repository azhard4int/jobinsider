from django.db import models

# Create your models here.

class Admin(models.Model):
    admin_username = models.CharField(
        blank=True,
        max_length=255,
        default=None
    )
    admin_password = models.CharField(
        blank=True,
        max_length=255,
        default=None
    )
    admin_status = models.CharField(
        blank=True,
        max_length=255,
        default=0
    )   # this is mainly for different roles
    admin_last_login = models.DateTimeField(
        blank=True,
        max_length=255,
        default=None
    )
    admin_login_ip = models.IPAddressField(
        blank=True,
        default=None,
    )   # we will restrict admin based on their ip zone.
    admin_is_active = models.BooleanField(
        blank=True,
        default=0
    )   # in order to disable other admins.

    admin_session = models.CharField(
        blank=True,
        default=None,
        max_length=255
    )

