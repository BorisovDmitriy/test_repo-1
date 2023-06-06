from django.http import HttpResponse
from django.shortcuts import render

def index(request): #HttpRequest название любое, сылка на request обязательна
    return HttpResponse('Старница приложения women')

def categories(request):
    return HttpResponse("<h1>Статья по категориям/<h1>")