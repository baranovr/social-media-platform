from user.views import (
    CreateUserView,
    MyProfileView,
    CreateTokenView, UserListView,
)

from django.urls import path


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", MyProfileView.as_view(), name="manage-me"),
    path("users/", UserListView.as_view(), name="users"),
]


app_name = "user"
