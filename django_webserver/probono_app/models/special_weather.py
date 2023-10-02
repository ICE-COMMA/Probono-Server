from django.db import models

class SpecialWeather(models.Model):
    TM_EF   = models.CharField(max_length=50)
    REG_NM  = models.CharField(max_length=100)
    WRN     = models.CharField(max_length=100)
    LVL     = models.CharField(max_length=50)

    class Meta:
        db_table = 'special_weather'

    def __str__(self):
        return f"{self.REG_NM} - {self.WRN} ({self.LVL})"