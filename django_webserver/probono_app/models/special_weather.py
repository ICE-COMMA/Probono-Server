from django.db import models

class SpecialWeather(models.Model):
    TM_EF = models.CharField(max_length=50)  # 효력 발휘 시각
    REG_NM = models.CharField(max_length=100)  # 지역 이름 (예: 서울동남권)
    WRN = models.CharField(max_length=100)  # 특보 종류 (예: 강풍, 호우 등)
    LVL = models.CharField(max_length=50)  # 특보 레벨 (예: 예비, 주의보, 경보)

    class Meta:
        db_table = 'special_weather'

    def __str__(self):
        return f"{self.REG_NM} - {self.WRN} ({self.LVL})"