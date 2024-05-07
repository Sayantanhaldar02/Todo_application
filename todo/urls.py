from django.urls import path
from todo.views import *

urlpatterns = [
    path("", create_todo,name="create_todo"),
    path("all-todo/", all_todo,name="all_todo"),
    path("update/<id>/", update_todo,name="update_todo"),
    path("delete/<id>/", delete_todo,name="delete_todo"),
    path("completed/<id>/", mark_as_complete,name="mark_as_complete"),
    path("completed/", complete_todo,name="complete_todo"),
    path("login/", user_login,name="user_login"),
    path("register/", user_register,name="user_register"),
    path("logout/", user_logout,name="user_logout"),
]
