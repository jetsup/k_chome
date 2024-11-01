from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from k_chome.utils import get_site_url

def home(request: HttpRequest) -> HttpResponse:
    # redirect user if not logged in
    if not request.user.is_authenticated:
        return redirect("auth")
    
    return render(
        request,
        'index.html', 
        {"year": datetime.now().year}
    )
