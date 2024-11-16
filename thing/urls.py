from django.urls import path
from .views import ThingListCreate, ThingDelete
from .views import get_connected_boards

urlpatterns = [
    path("", ThingListCreate.as_view(), name="thing-list-create"),
    path("delete/<int:pk>/", ThingDelete.as_view(), name="thing-delete"),
    path("add-thing/", ThingListCreate.as_view(), name="add-thing"),
    path("connected-boards/", get_connected_boards, name="connected-boards"),
]
