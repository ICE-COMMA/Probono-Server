from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def my_page(request):
    return render(request, 'my_page.html')

