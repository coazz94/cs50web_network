
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("following_page", views.following_page, name="following_page"),
    path("user_page/<int:user_id>", views.user_page, name="user_page"),
    path("change_follow(<int:user_searched_id>", views.change_follow, name="change_follow"),

    ]