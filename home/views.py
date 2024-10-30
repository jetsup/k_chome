from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from datetime import datetime

def home(request: HttpRequest) -> HttpResponse:
    # redirect user if not logged in
    if not request.user.is_authenticated:
        return redirect("authenticate")
    
    return render(
        request,
        'index.html', 
        {"year": datetime.now().year}
    )
