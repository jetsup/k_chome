from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from k_auth.models import HomeUsers, UserTypes
from k_auth.constants import USER_TYPES
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import HomeUserSerializer


# Create API Create User view
class CreateUserView(generics.CreateAPIView):
    queryset = HomeUsers.objects.all()
    serializer_class = HomeUserSerializer
    permission_classes = [AllowAny]


def register(request: HttpRequest):  # register function called through API
    if request.method == "POST":
        data = request.POST

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        password_confirm = data.get("password_confirm")
        toc = data.get("terms")

        if not first_name:
            return JsonResponse({"error": "First name is required"}, status=400)
        if not last_name:
            return JsonResponse({"error": "Last name is required"}, status=400)
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)
        if not password:
            return JsonResponse({"error": "Password is required"}, status=400)
        if not password_confirm:
            return JsonResponse(
                {"error": "Password confirmation is required"}, status=400
            )
        if not toc:
            return JsonResponse(
                {"error": "Terms and conditions must be accepted"}, status=400
            )

        if password != password_confirm:
            return JsonResponse({"error": "Passwords do not match"}, status=400)

        if HomeUsers.objects.filter(email=email).exists():
            return JsonResponse(
                {"error": "User with this email already exists"}, status=400
            )

        user_type = UserTypes.objects.get_or_create(user_type=USER_TYPES[0])[0]
        user = HomeUsers.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            password=password,
            user_type=user_type,
        )

        if user:
            print(f"API User registered: {user}")
            return JsonResponse({"success": "User registered successfully"}, status=200)
