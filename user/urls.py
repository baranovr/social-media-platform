from user.views import (
    CreateUserView,
    UserProfileView,
    UserListView,
    SubscribeView,
    SubscriberListView,
    SubscriptionsListView,
    UnsubscribeView,
    PostListView,
    UserPostDetailView,
    CreateTokenView,
)

from user.logout import logout_view

from django.urls import path

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", UserProfileView.as_view(), name="manage-me"),
    path("me/logout/", logout_view, name="logout"),
    path("me/posts/", PostListView.as_view(), name="user-posts"),
    path(
        "me/posts/<id>/",
        UserPostDetailView.as_view(),
        name="user-posts"
    ),
    path(
        "me/subscribers/",
        SubscriberListView.as_view(),
        name="subscriber-list"
    ),
    path(
        "me/subscriptions/",
        SubscriptionsListView.as_view(),
        name="subscribed-list"
    ),
    path(
        "me/subscriptions/<int:pk>/unsubscribe/",
        UnsubscribeView.as_view(),
        name="unsubscribe"
    ),
    path("users/", UserListView.as_view(), name="users"),
    path(
        "users/<int:user_id>/subscribe/",
        SubscribeView.as_view(),
        name="subscribe"
    ),
]

app_name = "user"
