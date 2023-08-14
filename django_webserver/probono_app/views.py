from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'index.html')

def my_page(request):
    return render(request, 'my_page.html')

def transfer_info(request):
    return render(request, 'transfer.html')

def transfer_info(request):
    return render(request, 'transfer.html')

def weather_info(request):
    return render(request, 'transfer.html')

def dense_popul_info(request):
    return render(request, 'transfer.html')

def dense_popul_info(request):
    return render(request, 'transfer.html')

def safety_info(request):
    return render(request, 'transfer.html')

def login_view(request):
    return render(request, 'transfer.html')

def sign_up(request):
    return render(request, 'transfer.html')

def logout_view(request):
    return render(request, 'transfer.html')