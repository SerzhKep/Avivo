from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Главная страница!')


def product(request):
    return HttpResponse('Товары!')