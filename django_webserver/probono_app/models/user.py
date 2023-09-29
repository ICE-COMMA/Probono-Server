from django.db import models

class CustomPreferences(models.Model):
    custom_demo = models.BooleanField(default=False)
    custom_elevator = models.BooleanField(default=False)
    custom_population = models.BooleanField(default=False)
    custom_predict = models.BooleanField(default=False)
    custom_safety = models.BooleanField(default=False)
    custom_safety_loc = models.BooleanField(default=False)
    custom_low_bus = models.BooleanField(default=False)
    custom_festival = models.BooleanField(default=False)

class User(models.Model):
    ID = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    PW = models.CharField(max_length=50) # In practice, never save plain passwords. Use Django's User model & authentication system.
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
    date = models.DateField(null=True, blank=True) # Birthdate maybe?
    impaired = models.CharField(max_length=100, null=True, blank=True) # Assuming it's a string, but not sure of its content
    custom = models.OneToOneField(CustomPreferences, on_delete=models.CASCADE)

    class Meta:
        db_table = 'User'