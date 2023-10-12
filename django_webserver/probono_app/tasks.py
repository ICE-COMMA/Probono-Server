from celery import shared_task
from .services import SubwayInfo, SpecialWeatherService, SafetyGuardHouseInfo, DemoInfo, BusInfo

'''
서버 구동 후, 반드시 터미널 창 두개 열어서 실행해야 함.

celery -A your_project worker -l info
celery -A your_project beat -l info
'''

@shared_task
def update_subway_elvtr():
    subway_elevator = SubwayInfo()
    subway_elevator.get_subway_elvtr_task()
    return


@shared_task
def get_bus_no_to_route():
    bus = BusInfo()
    bus.get_bus_no_to_route()
    return

@shared_task
def update_safety_guard_house_task():
    safety_guard_house = SafetyGuardHouseInfo()
    safety_guard_house.get_safety_guard_house()
    return
    

@shared_task
def update_special_weather_task():
    special_weather = SpecialWeatherService()
    special_weather.update_special_weather()
    return


@shared_task
def update_demo_task():
    demo = DemoInfo()
    demo._crawling_demo()
    return