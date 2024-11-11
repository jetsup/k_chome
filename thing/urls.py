from django.urls import path
from .views import ThingListCreate, ThingDelete

urlpatterns = [
    path('', ThingListCreate.as_view(), name='thing-list-create'),
    path('delete/<int:pk>/', ThingDelete.as_view(), name='thing-delete'),
]
 