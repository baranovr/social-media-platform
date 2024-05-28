from django.urls import path

from user.views import (
    CreateUserView,
    UserProfileView,
    UserSearchListView,
    SubscribeView,
    SubscriberListView,
    SubscriptionsListView,
    PostListView,
    UserPostDetailView,
    CreateTokenView,
    UserSearchDetailView,
    SubscriptionsDetailView,
    SubscribersDetailView,
    PostUserListView,
)
from user.logout import logout_view


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", UserProfileView.as_view(), name="manage-me"),
    path("me/logout/", logout_view, name="logout"),
    path("me/posts/", PostUserListView.as_view(), name="user-posts"),
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
        "me/subscribers/<int:pk>/",
        SubscribersDetailView.as_view(),
        name="subscriber-list"
    ),
    path(
        "me/subscriptions/",
        SubscriptionsListView.as_view(),
        name="subscribed-list"
    ),
    path(
        "me/subscriptions/<int:pk>/",
        SubscriptionsDetailView.as_view(),
        name="subscribed-detail"
    ),
    path("users/", UserSearchListView.as_view(), name="users"),
    path("users/<int:pk>/", UserSearchDetailView.as_view(), name="profile"),
    path(
        "users/<int:user_id>/subscribe/",
        SubscribeView.as_view(),
        name="subscribe"
    ),
]

app_name = "user"
