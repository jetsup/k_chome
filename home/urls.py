from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("boards", views.boards, name="boards"),
    path("online-boards", views.online_boards, name="boards-online"),
    path("boards/add", views.add_board, name="board-add"),
    path("boards-update/<int:pk>/", views.update_board, name="board-update"),
    path("boards-delete/<int:pk>/", views.delete_board, name="board-delete"),
]
