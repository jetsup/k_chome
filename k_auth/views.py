from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from .models import HomeUsers, UserTypes, VerificationTokens
import uuid
from .constants import USER_TYPES

SESSION_EXPIRY = 1209600  # 2 weeks


def auth(request: HttpRequest) -> HttpResponse:
    return render(
        request, "security/login_register.html", {"year": datetime.now().year}
    )


def signin(request: HttpRequest) -> HttpResponse:
    username = request.POST.get("username")
    password = request.POST.get("password")
    remember_me = request.POST.get("remember_me") == "on"

    if not username:
        messages.error(request, "Username is required")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )
    if not password:
        messages.error(request, "Password is required")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )

    user = authenticate(username=username, password=password)
    print(f"User: {user}")

    if user is not None:
        if not user.is_verified:
            messages.error(
                request,
                "Account not verified. Please check your email for verification link",
            )
            return render(
                request, "security/login_register.html", {"year": datetime.now().year}
            )

        if remember_me:
            request.session.set_expiry(SESSION_EXPIRY)
        else:
            request.session.set_expiry(0)  # after browser close

        login(request, user)
        return redirect("home")
    else:
        messages.error(request, "Invalid username or password")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )


def account_confirmation(request: HttpRequest) -> HttpResponse:
    return render(
        request, "security/account_confirmation.html", {"year": datetime.now().year}
    )


def signup(request: HttpRequest) -> HttpResponse:
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    password_confirmation = request.POST.get("password_confirmation")
    toc = request.POST.get("terms")

    if not first_name:
        messages.error(request, "First name is required")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )
    if not last_name:
        messages.error(request, "Last name is required")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )
    if not email:
        messages.error(request, "Email is required")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )
    if not password:
        messages.error(request, "Password is required")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )
    if not password_confirmation:
        messages.error(request, "Password confirmation is required")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )

    # check if passwords match
    if password != password_confirmation:
        messages.error(request, "Passwords do not match")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )

    # check if terms and conditions are accepted
    if not toc:
        messages.error(request, "Please accept the terms and conditions")
        return render(
            request, "security/login_register.html", {"year": datetime.now().year}
        )

    user_type = UserTypes.objects.get_or_create(user_type=USER_TYPES[0])[0]

    # create user
    if not messages.get_messages(request):
        try:
            user = HomeUsers.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,
                password=password,
                user_type=user_type,
            )

            if user:
                user.save()
                messages.success(request, "User created successfully")
                print("User created successfully")
                response_code = user.send_verification_email(request)

                if response_code == 200:
                    return redirect(
                        "account-confirmation",
                        {
                            "year": datetime.now().year,
                            "confirmation_message": "Verification code has been sent to your email",
                        },
                    )
                else:
                    messages.error(
                        request,
                        f"Failed to send verification email to {email}. Error code: {response_code}",
                    )
                    return render(
                        request,
                        "security/login_register.html",
                        {
                            "year": datetime.now().year,
                            "message": f"Failed to send verification email to {email}. Error code: {response_code}",
                        },
                    )
            else:
                messages.error(request, "User not created")
                print("User not created")
                return render(
                    request,
                    "security/login_register.html",
                    {"year": datetime.now().year},
                )
        except Exception as e:
            messages.error(request, f"User not created. {str(e)}")
            print(f"User not created. {str(e)}")
            return render(
                request, "security/login_register.html", {"year": datetime.now().year}
            )


def verify_account(request: HttpRequest, token: uuid) -> HttpResponse:
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in")
        return redirect("home")

    verification_token = VerificationTokens.objects.get(token=token)
    if verification_token.is_expired:
        messages.error(
            request,
            f"Verification code has expired. A new one has been sent to your email",
        )
        user = HomeUsers.objects.get(verification_token=verification_token)
        user.send_verification_email(request)
        return redirect(
            "account-confirmation",
            {
                "year": datetime.now().year,
                "confirmation_message": "Verification code has expired. A new one has been sent to your email",
            },
        )

    user = HomeUsers.objects.get(verification_token=verification_token)
    if not user:
        messages.error(request, "User not found")
        return redirect("home")

    if user.is_verified:
        messages.error(request, "Account already verified")
        return redirect("home")

    user.is_verified = True
    user.verified_at = datetime.now()
    user.save()

    verification_token.is_expired = True
    verification_token.save()

    messages.success(request, "Account verified successfully")
    return redirect("home")


def signout(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")


def forgot_password(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Email is required")
            return render(
                request, "security/forgot_password.html", {"year": datetime.now().year}
            )

        user = HomeUsers.objects.get(email=email)
        if not user:
            messages.error(request, "User not found")
            return render(
                request, "security/forgot_password.html", {"year": datetime.now().year}
            )

        response_code = user.send_password_reset_email(request)
        if response_code == 200:
            messages.success(request, "Verification code has been sent to your email")

            return render(
                request,
                "security/change_password.html",
                {
                    "year": datetime.now().year,
                    "message": "Password reset URL has been sent to your email",
                },
            )
        else:
            messages.error(
                request,
                f"Failed to send reset URL to {email}. Error code: {response_code}",
            )
            return render(
                request,
                "security/forgot_password.html",
                {
                    "year": datetime.now().year,
                    "message": f"Failed to send reset URL to {email}. Error code: {response_code}",
                },
            )

    # GET request
    return render(
        request, "security/forgot_password.html", {"year": datetime.now().year}
    )


def change_password(request: HttpRequest, reset_token: uuid) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        verification_code = request.POST.get("verification_code")

        if not email:
            messages.error(request, "Email is required")
            return render(
                request, "security/change_password.html", {"year": datetime.now().year}
            )
        if not password:
            messages.error(request, "Password is required")
            return render(
                request, "security/change_password.html", {"year": datetime.now().year}
            )
        if not password_confirmation:
            messages.error(request, "Password confirmation is required")
            return render(
                request, "security/change_password.html", {"year": datetime.now().year}
            )

        # check if passwords match
        if password != password_confirmation:
            messages.error(request, "Passwords do not match")
            return render(
                request, "security/change_password.html", {"year": datetime.now().year}
            )

        user = HomeUsers.objects.get(email=email)
        if not user:
            messages.error(request, "User not found")
            return render(
                request, "security/change_password.html", {"year": datetime.now().year}
            )

        user.set_password(password)
        user.save()

        messages.success(request, "Password changed successfully")
        return redirect("auth")

    # GET
    return render(
        request, "security/change_password.html", {"year": datetime.now().year}
    )


def tac(request: HttpRequest) -> HttpResponse:
    return render(request, "privacy/tac.html", {"year": datetime.now().year})


#
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "security/profile.html", {"year": datetime.now().year})
