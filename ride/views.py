from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.


def home(request):
    return render(request,'ride/home.html')


def view_requests(request):
    return render(request, 'ride/home.html')


def request_new(request):
    return render(request, 'ride/home.html')


def driver_home(request):
    return render(request, 'ride/home.html')


def sharer_request_new(request):
    return render(request, 'ride/home.html')
