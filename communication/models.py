from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.conf import settings

# Hold email addresses
class EmailAddress(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email
    
class EmailMessage(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    # a list of recipients
    recipients = models.ManyToManyField(EmailAddress)
    sender = models.EmailField(default=settings.EMAIL_HOST_USER)
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def send(self):
        subject = self.subject
        message = self.message
        sender = self.sender
        recipients = [recipient.email for recipient in self.recipients.all()]
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=sender,
            to=recipients
        )
        
        stat = email.send()

        if stat != 0:
            self.sent = True
            self.save()
            
            return HttpResponse('Email sent')
        else:
            return HttpResponse('Email not sent')
    
    def __str__(self):
        return self.subject
