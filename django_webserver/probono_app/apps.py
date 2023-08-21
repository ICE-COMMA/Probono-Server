from django.apps import AppConfig


class ProbonoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'probono_app'

    def ready(self):
        from config import utils
        from .models import SpecialWeather

        db_handle = utils.db_handle
        get_collection = utils.get_collection_handle
        
        spw_ins = SpecialWeather()
        collection = get_collection(db_handle, 'special_weather')
        # spw_ins.init_special_weather(collection)