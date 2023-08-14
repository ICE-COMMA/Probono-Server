from django.shortcuts import render, redirect
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
    return render(request, 'login.html')

def sign_up(request):
    return render(request, 'transfer.html')

def logout_view(request):
    return render(request, 'transfer.html')