from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
#
# class CustomPreferences(models.Model):
#     custom_demo         = models.BooleanField(default=False)
#     custom_elevator     = models.BooleanField(default=False)
#     custom_population   = models.BooleanField(default=False)
#     custom_predict      = models.BooleanField(default=False)
#     custom_safety       = models.BooleanField(default=False)
#     custom_safety_loc   = models.BooleanField(default=False)
#     custom_low_bus      = models.BooleanField(default=False)
#     custom_festival     = models.BooleanField(default=False)
#
# class ProbonoUserManager(BaseUserManager):
#     def create_user(self, ID, password=None, **extra_fields):
#         if not ID:
#             raise ValueError("The ID field must be set")
#         user = self.model(ID=ID, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, ID, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self.create_user(ID, password, **extra_fields)
#
# class ProbonoUser(AbstractBaseUser, PermissionsMixin):
#     ID          = models.CharField(max_length=100, unique=True)
#     name        = models.CharField(max_length=100)
#     gender      = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
#     date        = models.DateField(null=True, blank=True)
#     impaired    = models.CharField(max_length=50, null=True, blank=True)
#     custom      = models.OneToOneField(CustomPreferences, on_delete=models.CASCADE)
#
#     USERNAME_FIELD  = "ID"
#     REQUIRED_FIELDS = []
#
#     objects = ProbonoUserManager()
#
#     class Meta:
#         db_table = 'ProbonoUser'