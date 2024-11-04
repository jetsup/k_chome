from django.urls import path
from . import views
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView, UserDetailsView

urlpatterns = [
    path('login', LoginView.as_view(), name='api-login'),
    path('logout', LogoutView.as_view(), name='api-logout'),
    path('password-reset', PasswordResetView.as_view(), name='api-password-reset'),
    path('password-reset-confirm', PasswordResetConfirmView.as_view(), name='api-password-reset-confirm'),
    path('password-change', PasswordChangeView.as_view(), name='api-password-change'),
    path('user-details', UserDetailsView.as_view(), name='api-user-details'),
    path('register', views.register, name='api-register'),
]
 