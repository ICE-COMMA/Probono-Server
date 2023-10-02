from django.db import models

class SubwayElevator(models.Model):
    sw_nm   = models.CharField(max_length=255, verbose_name="Name")
    x       = models.FloatField(verbose_name="Longitude")
    y       = models.FloatField(verbose_name="Latitude")

    class Meta:
        db_table = 'subway_elevator'