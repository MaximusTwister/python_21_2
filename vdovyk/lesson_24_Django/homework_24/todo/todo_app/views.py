from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest):
    print(f'{request}')
    return HttpResponse('Hello from Django')


def index(request: HttpRequest):
    print(f'{request}')
    return HttpResponse('Start page')

