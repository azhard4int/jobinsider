__author__ = 'azhar'

# class UserAccount(AbstractBaseUser):
#     username = models.CharField(
#         max_length=255,
#         unique=True,
#     )
#
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     first_name = models.CharField(
#         max_length=120,
#         null=True,
#         blank=True,
#     )
#     last_name = models.CharField(
#         max_length=120,
#         null=True,
#         blank=True,
#     )
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     USERNAME_FIELD = username
#     REQUIRED_FIELDS = ['email']
#
#     def get_username(self):
#         return self.username
#
#     def get_email(self):
#         return self.email
#
#     def get_first_name(self):
#         return self.first_name
#
#     def get_last_name(self):
#         return self.last_name
#
