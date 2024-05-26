from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, generics, permissions
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.response import Response

from social_media.serializers import (
    HashtagSerializer,
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
    DislikeDetailSerializer,
    SubscribedPostListSerializer,
    SubscribedPostDetailSerializer,
    LikedPostSerializer,
    DislikedPostSerializer
)

from social_media.models import (
    Hashtag,
    Post,
    Comment,
    Like,
    Dislike,
    Subscription
)


class HashtagListCreateView(generics.ListCreateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = (IsAuthenticated,)


class HashtagDeleteView(generics.DestroyAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = (IsAdminUser,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.AllowAny()]
        elif self.action == "retrieve":
            return [permissions.IsAuthenticatedOrReadOnly()]
        else:
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        username = self.request.query_params.get("user__username", None)
        title = self.request.query_params.get("title", None)
        date_posted = self.request.query_params.get("date_posted", None)
        tags = self.request.query_params.getlist("tags[]", None)

        queryset = self.queryset

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if date_posted:
            date_p = datetime.strptime(date_posted, "%Y-%m-%d").date()
            queryset = queryset.filter(date_posted__date=date_p)
            return queryset

        if tags:
            queryset = queryset.filter(tags__name__in=tags)
            return queryset

        queryset = queryset.filter(published=True)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        return PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"], user=request.user)
        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        author = post.user

        if author != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return super().destroy(request, *args, **kwargs)


class SubscribedPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscribedPostListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        subscribed_users = (
            Subscription.objects.filter(subscriber=user).
            values_list("subscribed", flat=True)
        )
        return (
            Post.objects.filter(user__in=subscribed_users).
            order_by("-date_posted")
        )

    def get_serializer_class(self):
        if self.action == "list":
            return SubscribedPostListSerializer

        if self.action == "retrieve":
            return SubscribedPostDetailSerializer


class LikedPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LikedPostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(like__user=user)


class DislikedPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DislikedPostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(dislike__user=user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs["pk"])
        author = comment.user

        if author != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs["pk"])
        post = get_object_or_404(Post, pk=kwargs["pk"])
        author = comment.user
        poster = post.user

        if author != request.user or poster != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().destroy(request, *args, **kwargs)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        like = get_object_or_404(Like, pk=kwargs["pk"])
        liker = like.user

        if liker != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().destroy(request, *args, **kwargs)


class DislikeViewSet(viewsets.ModelViewSet):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        like = get_object_or_404(Dislike, pk=kwargs["pk"])
        liker = like.user

        if liker != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        like = get_object_or_404(Like, pk=kwargs["pk"])
        liker = like.user

        if liker != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().destroy(request, *args, **kwargs)
