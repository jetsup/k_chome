from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.http import HttpRequest
import uuid
import pyotp
from django.conf import settings
from k_chome.utils import get_site_url
from communication.controller import send_email
from datetime import datetime, timedelta
from django.contrib import messages

OTP_TIMEOUT = 300  # 5 minutes
TOKEN_EXPIRATION = 1800  # 30 minutes

class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name: str,
        last_name: str,
        id_passport_number: str,
        phone: str,
        email: str|None,
        password=None,
    ):
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not phone:
            raise ValueError("Users must have a phone number")
        # if not email:
        #     raise ValueError("Users must have an email")
        if not id_passport_number:
            raise ValueError("Users must have an ID/Passport number")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        first_name,
        last_name,
        email,
        location_address,
        phone=None,
        password=None,
    ):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=self.normalize_email(email),
            location_address=location_address,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserTypes(models.Model):
    user_type = models.CharField(max_length=10) # customer, admin, staff

    def __str__(self):
        return self.user_type


class VerificationTokens(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    expires_at = models.DateTimeField()
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expires_at = datetime.now() + timedelta(seconds=TOKEN_EXPIRATION)

    def __str__(self):
        return f"Token: {self.token} expire(s/d) at {self.expires_at}"


class HomeUsers(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    dp = models.ImageField(upload_to="dp", blank=True, default=None, null=True)
    user_type = models.ForeignKey(
        UserTypes, on_delete=models.SET_NULL, null=True, default=None
    )
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True, default=None)
    # verification code will be nullified after verification or after 24 hours
    verification_token = models.OneToOneField(VerificationTokens, on_delete=models.SET_NULL, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email + " : " + self.first_name + " " + self.last_name

    def groups(self):
        pass

    def user_permissions(self):
        pass

    def generate_totp_token(self) -> str:
        totp = pyotp.TOTP(self.verification_code, interval=OTP_TIMEOUT)
        return totp.now()

    def verify_totp_token(self, token: str) -> bool:
        totp = pyotp.TOTP(self.verification_code, interval=OTP_TIMEOUT)
        return totp.verify(token)

    def send_verification_email(self, request: HttpRequest):
        self.verification_token = VerificationTokens.objects.create()
        
        site_url = get_site_url(request)
        verification_link = f"{site_url}/verify/{str(self.verification_token.token)}"
        email_subject = "Email Verification"
        email_message = f"""
        You have created an account on {settings.PROJECT_SITE_NAME}. Please verify your email by clicking the link below to complete your registration.

        {verification_link}

        If you did not request this, please ignore this email.

        Regards,
        {settings.PROJECT_SITE_NAME}
        """
        response_code = send_email([self.email], email_subject, email_message)
        print(f"Email sent to {self.email}. Response: {response_code}")

        if response_code == 200:
            self.save()
        else:
            messages.error(request, f"Failed to send verification email to {self.email}. Error code: {response_code}")

        return response_code

    class Meta:
        swappable = "AUTH_USER_MODEL"
