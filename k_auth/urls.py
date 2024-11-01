from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth, name='auth'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('verify/<str:token>', views.verify_account, name='verify-account'),
    path('signout', views.signout, name='signout'),
    path('reset_password', views.forgot_password, name='forgot-password'),
    path('change_password', views.change_password, name='change-password'),
    path('tac', views.tac, name='tac'),
]
