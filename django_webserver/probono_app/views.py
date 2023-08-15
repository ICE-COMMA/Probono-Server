from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUserManager
from config import utils

def index(request):
    return render(request, 'index.html')

def my_page(request):
    return render(request, 'my_page.html')

def transfer_info(request):
    return render(request, 'transfer_info.html')

def weather_info(request):
    return render(request, 'weather_info.html')

def dense_popul_info(request):
    return render(request, 'dense_popul_info.html')

def safety_info(request):
    return render(request, 'safety_info.html')

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('username') # WARN : front's parameter name
        password = request.POST.get('password')
        user = authenticate(request, user_id=user_id, password=password) # REMIND : This code have to verified by backend
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')

def sign_up(request):

    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('index')