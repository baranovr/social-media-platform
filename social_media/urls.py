from rest_framework import routers

from django.urls import path

from social_media import views
from social_media.views import (
    HashtagListCreateView,
    HashtagDeleteView,
    SubscribedPostViewSet
)


router = routers.DefaultRouter()

router.register("posts", views.PostViewSet, basename="posts")
router.register(
    "subscribed-posts",
    SubscribedPostViewSet,
    basename="subscribed-posts"
),
router.register("comments", views.CommentViewSet, basename="comments")
router.register("likes", views.LikeViewSet, basename="likes")
router.register("dislikes", views.DislikeViewSet, basename="dislikes")

urlpatterns = [
    path("hashtags/", HashtagListCreateView.as_view(), name="tag-list"),
    path("hashtags/<int:pk>/", HashtagDeleteView.as_view(), name="tag-del"),
] + router.urls


app_name = "social_media"
