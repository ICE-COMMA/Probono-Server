"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from probono_app import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('my_page/<str:id>', views.my_page, name='my_page'),
    path('transfer_info/', views.transfer_info, name='transfer_info'),
    path('weather_info/', views.weather_info, name='weather_info'),
    path('dense_popul_info', views.dense_popul_info, name='dense_popul_info'),
    path('safety_info', views.safety_info, name='safety_info'),
    path('login/', views.login_view, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
    path('id_check', views.id_check, name='id_check'),
    path('get_subway_elvtr/', views.get_subway_elvtr, name='get_subway_elvtr'),
    path('get_safety_guard_house/',views.get_safety_guard_house,name='get_safety_guard_house'),
    path('get_bus_no_to_route/', views.get_bus_no_to_route, name='get_bus_no_to_route'),
    path('get_bus_route/<str:bus_num>', views.get_bus_route, name='get_bus_route'),
    path('get_demo_today/', views.get_demo_today, name='get_demo_today'),
    path('get_hwp_text/',views.get_hwp_text,name='get_hwp_text')
]