from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

# Mongo DB
from config import utils

# Session
from django.contrib.auth import authenticate, login, logout

# User
from .models import CustomUserManager, CustomUser
from .forms import SignUpForm


db_handle = utils.db_handle
get_collection = utils.get_collection_handle

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

@require_POST
def sign_up(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        users = get_collection(db_handle, 'User')
        users.insert_one(form)
    return redirect('index')

@require_POST
def id_duplicate(request):
    users = get_collection(db_handle, 'User')
    temp = users.find_one({'ID' : request.form['check_id']})
    if temp:
        data = { "message": "id duplicated" } # REMIND : front have to know its response.
        status_code = 201
    else:
        data = { "message": "id ok" }
        status_code = 201
    return JsonResponse(data, status=status_code)

def logout_view(request):
    logout(request)
    return redirect('index')