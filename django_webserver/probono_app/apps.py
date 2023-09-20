from django.apps import AppConfig


class ProbonoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'probono_app'

    def ready(self):
        from config import utils
        from .models import SpecialWeather, DemoScraper, Population_real_time

        db_handle = utils.db_handle
        get_collection = utils.get_collection_handle

        import os
        
        if os.environ.get('RUN_MAIN') == 'true':
            '''
            spw_ins = SpecialWeather()
            collection = get_collection(db_handle, 'special_weather')
            spw_ins.init_special_weather(collection)
            '''

            demo = DemoScraper()
            collection = get_collection(db_handle, 'demo')
            demo.get_demo(collection)

            prt = Population_real_time()
            collection = get_collection(db_handle, 'popul_real_time_reg')
            prt.init_population_info(collection)