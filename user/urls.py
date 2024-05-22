from user.views import CreateUserView, ManageUserView, CreateTokenView

from django.urls import path


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="manage-me"),
]


app_name = "user"
