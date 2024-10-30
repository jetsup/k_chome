from django.urls import path
from . import views

urlpatterns = [
    path('', views.authenticate, name='authenticate'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('reset_password', views.forgot_password, name='forgot-password'),
    path('change_password', views.change_password, name='change-password'),
    path('tac', views.tac, name='tac'),
]
