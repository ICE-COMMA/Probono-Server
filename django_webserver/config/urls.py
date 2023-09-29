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

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api/', views.index, name='index'),
    # path('api/my_page/<str:id>/', views.my_page, name='my_page'),
    # path('api/dense_popul_info/real/', views.real_dense_popul_info, name='real_popul_info'),
    # path('api/dense_popul_info/predict/', views.predict_dense_popul_info, name='predict_popul_info'),
    path('api/safety_info/data/', views.SafetyGuardHouseListView.as_view(), name='safety_info_data'),
    # path('api/login/', views.login_view, name='login'),
    # path('api/sign_up/', views.sign_up, name='sign_up'),
    # path('api/logout/', views.logout_view, name='logout'),
    # path('api/id_check/', views.id_check, name='id_check'),
    # path('api/custom/', views.update_custom, name='update_custom'),
    # path('api/get_subway_elvtr/<str:subway_station>/', views.get_subway_elvtr, name='get_subway_elvtr'),
    # path('api/get_bus_route/<str:bus_num>/', views.get_bus_route, name='get_bus_route'),
    # path('api/get_bus_pos/<str:route_id>/', views.get_bus_pos, name='get_bus_pos'),
    # path('api/get_demo_today/', views.get_demo_today, name='get_demo_today'),
    # path('api/popul_test/', views.test_AI, name='test_AI'),
]