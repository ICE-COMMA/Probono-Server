from django.db import models

class PopulRegion(models.Model):
    CATEGORY    = models.CharField(max_length=255)
    NO          = models.PositiveIntegerField()
    AREA_CD     = models.CharField(max_length=50, unique=True)
    AREA_NM     = models.CharField(max_length=255)

    class Meta:
        db_table = 'popul_real_time_reg'