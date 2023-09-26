from django.apps import AppConfig


class ProbonoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'probono_app'

    def ready(self):
        from config import utils
        from .models import SpecialWeather, DemoInfo, PopulationRealTime

        import os
        
        if os.environ.get('RUN_MAIN') == 'true':
            spw_ins = SpecialWeather()
            spw_ins.init_special_weather()

            demo = DemoInfo()
            demo._crawling_demo()

            prt = PopulationRealTime()
            prt.init_population_info()