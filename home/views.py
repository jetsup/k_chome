from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from communication.models import EmailMessage, EmailAddress
from communication.controller import send_email

def home(request: HttpRequest) -> HttpResponse:
    
    # Test Email send functionality
    recipient1 = "email1@gmail.com"
    recipient2 = "email2@gmail.com"

    subject = "Welcome to K Home System"
    message = "Hello, welcome to K Home System. We are glad to have you here."
    
    response = send_email([recipient1, recipient2], subject, message)
    
    return render(request, 'index.html')
