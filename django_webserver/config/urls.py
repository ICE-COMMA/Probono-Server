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
    path('api/auth/sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('api/auth/login/', views.LoginView.as_view(), name='login'),
    path('api/auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/auth/user/', views.UserView.as_view(), name='user'),
    path('api/auth/id_check/', views.id_check, name='id_check'),


    # path('api/', views.index, name='index'),
    # path('api/my_page/<str:id>/', views.my_page, name='my_page'),
    path('api/dense_popul_info/real/', views.real_dense_popul_info, name='real_popul_info'),
    path('api/dense_popul_info/predict/', views.predict_dense_popul_info, name='predict_popul_info'),
    path('api/safety_info/data/', views.SafetyGuardHouseListView.as_view(), name='safety_info_data'),
    # path('api/custom/', views.update_custom, name='update_custom'),
    path('api/get_subway_elevator/<str:subway_station>/', views.get_subway_elevator, name='get_subway_elevator'),
    path('api/get_bus_route/<str:bus_num>/', views.get_bus_route, name='get_bus_route'),
    path('api/get_bus_pos/<str:route_id>/', views.get_bus_pos, name='get_bus_pos'),
    path('api/get_demo_today/', views.DemoListView.as_view(), name='get_demo_today'),
    # path('api/popul_test/', views.test_AI, name='test_AI'),
]