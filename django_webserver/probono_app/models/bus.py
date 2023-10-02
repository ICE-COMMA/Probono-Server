from django.db import models

class Bus(models.Model):
    bus_no  = models.CharField(max_length=20)
    route   = models.CharField(max_length=20)

    class Meta:
        db_table = 'bus'