from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from datetime import datetime

def authenticate(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'security/login_register.html',
        {"year": datetime.now().year}
    )

def signin(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'security/login_register.html',
        {"year": datetime.now().year}
    )

def signup(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'security/login_register.html',
        {"year": datetime.now().year}
    )

def signout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return render(
        request,
        'security/login_register.html',
        {"year": datetime.now().year}
    )

def forgot_password(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'security/forgot_password.html',
        {"year": datetime.now().year}
    )

def change_password(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'security/change_password.html',
        {"year": datetime.now().year}
    )

def tac(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'privacy/tac.html',
        {"year": datetime.now().year}
    )
