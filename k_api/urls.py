from django.urls import path, include

# from . import views
# from dj_rest_auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView, UserDetailsView
from .views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path('login', LoginView.as_view(), name='api-login'),
    # path('logout', LogoutView.as_view(), name='api-logout'),
    # path('password-reset', PasswordResetView.as_view(), name='api-password-reset'),
    # path('password-reset-confirm', PasswordResetConfirmView.as_view(), name='api-password-reset-confirm'),
    # path('password-change', PasswordChangeView.as_view(), name='api-password-change'),
    # path('user-details', UserDetailsView.as_view(), name='api-user-details'),
    # path('register', views.register, name='api-register'),
    #
    path("register/", CreateUserView.as_view(), name="api-auth-register"),
    path("token/", TokenObtainPairView.as_view(), name="api-token"),  # login
    path("token/refresh/", TokenRefreshView.as_view(), name="api-token-refresh"),
    path("api-auth/", include("rest_framework.urls")),
]
