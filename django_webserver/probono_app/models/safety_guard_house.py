from django.db import models

class SafetyGuardHouse(models.Model):
    name = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        db_table = 'safety_guard_house'