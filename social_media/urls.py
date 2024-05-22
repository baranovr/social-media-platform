from rest_framework import routers

from social_media import views

router = routers.DefaultRouter()

router.register("posts", views.PostViewSet, basename="posts")
router.register("comments", views.CommentViewSet, basename="comments")
router.register("likes", views.LikeViewSet, basename="likes")
router.register("dislikes", views.DislikeViewSet, basename="dislikes")

urlpatterns = router.urls


app_name = "social_media"
