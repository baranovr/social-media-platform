from user.views import CreateUserView, ManageUserView

from rest_framework.authtoken import views

from django.urls import path


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", views.obtain_auth_token, name="token"),
    path("me/", ManageUserView.as_view(), name="manage-me"),
]


app_name = "user"
