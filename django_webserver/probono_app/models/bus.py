from django.db import models

class Bus(models.Model):
    bus_no = models.CharField(max_length=50)
    route = models.CharField(max_length=100)

    class Meta:
        db_table = 'bus'