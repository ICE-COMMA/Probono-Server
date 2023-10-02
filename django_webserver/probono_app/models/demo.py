from django.db import models

class Demo(models.Model):
    location    = models.CharField(max_length=255)
    date        = models.DateField()
    time        = models.CharField(max_length=255)
    amount      = models.CharField(max_length=8)

    class Meta:
        db_table = 'demo'