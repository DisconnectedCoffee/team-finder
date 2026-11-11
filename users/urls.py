from django.urls import path
from .views import (
    participants_view,
    user_detail_view,
    register_view,
    login_view,
    logout_view,
    edit_profile_view,
    change_password_view,
)

app_name = "users"

urlpatterns = [
    path("list/", participants_view, name="participants_list"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("edit/", edit_profile_view, name="edit_profile"),
    path("edit-profile/", edit_profile_view, name="edit_profile_alias"),
    path("change-password/", change_password_view, name="change_password"),
    path("<int:pk>/", user_detail_view, name="user_detail"),
]
