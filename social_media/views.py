from datetime import datetime

from rest_framework import viewsets

from social_media.serializers import (
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    LikeSerializer,
    LikeListSerializer,
    DislikeSerializer,
    DislikeListSerializer,
    LikeDetailSerializer,
    DislikeDetailSerializer
)

from social_media.models import Post, Comment, Like, Dislike


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.request.query_params.get("user.username", None)
        title = self.request.query_params.get("title", None)
        date_posted = self.request.query_params.get(
            "date_posted", None
        )

        queryset = self.queryset

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if date_posted:
            date_p = datetime.strptime(date_posted, "%Y-%m-%d").date()
            queryset = queryset.filter(date_posted__date=date_p)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        return PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        username = self.request.query_params.get("user.username", None)
        post_title = self.request.query_params.get("post.title", None)
        created_at = self.request.query_params.get("created_at", None)

        queryset = self.queryset

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        if post_title:
            queryset = queryset.filter(title__icontains=post_title)

        if created_at:
            created = datetime.strptime(created_at, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__date=created)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer

        if self.action == "retrieve":
            return CommentDetailSerializer

        return CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        username = self.request.query_params.get("user.username", None)
        post_title = self.request.query_params.get("post.title", None)

        queryset = self.queryset

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        if post_title:
            queryset = queryset.filter(title__icontains=post_title)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return LikeListSerializer

        if self.action == "retrieve":
            return LikeDetailSerializer

        return LikeSerializer


class DislikeViewSet(viewsets.ModelViewSet):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer

    def get_queryset(self):
        username = self.request.query_params.get("user.username", None)
        post_title = self.request.query_params.get("post.title", None)

        queryset = self.queryset

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        if post_title:
            queryset = queryset.filter(title__icontains=post_title)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return DislikeListSerializer

        if self.action == "retrieve":
            return DislikeDetailSerializer

        return DislikeSerializer
