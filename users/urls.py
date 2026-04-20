from django.urls import path

from .views import (
    login_view,
    logout_view,
    register_view,
    user_detail_view,
    users_list_view,
)

app_name = "users"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("<int:user_id>/", user_detail_view, name="detail"),
    path("list/", users_list_view, name="list"),
]