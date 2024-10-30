from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

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

class HomeUsers(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    dp = models.ImageField(upload_to="dp", blank=True, default=None, null=True)
    user_type = models.ForeignKey(
        UserTypes, on_delete=models.SET_NULL, null=True, default=None
    )
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=10, null=True, blank=True, default=None)
    # verification code will be nullified after verification or after 24 hours
    verification_generation_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email + " : " + self.first_name + " " + self.last_name

    def groups(self):
        pass

    def user_permissions(self):
        pass

    class Meta:
        swappable = "AUTH_USER_MODEL"
