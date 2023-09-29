from django.db import models

class Demo(models.Model):
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.CharField(max_length=255)  # 시간 범위를 문자열로 표시
    amount = models.PositiveIntegerField()

    class Meta:
        db_table = 'demo'