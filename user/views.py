from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from social_media.serializers import (
    SubscribersListSerializer,
    SubscriptionsListSerializer,
    PostDetailSerializer,
    PostListSerializer,
    SubscriptionsDetailSerializer, SubscribersDetailSerializer
)

from social_media.models import Subscription, Post

from user.serializers import (
    UserSerializer,
    UserSearchListSerializer,
    UserProfileSerializer,
    UserSearchDetailSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class PostListView(generics.ListCreateAPIView):
    serializer_class = PostListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class UserPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class UserSearchListView(generics.ListAPIView):
    serializer_class = UserSearchListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        User = get_user_model()
        queryset = User.objects.all()

        username = self.request.query_params.get("username", None)
        user_id = self.request.query_params.get("user_id", None)

        if username:
            queryset = queryset.filter(username__icontains=username)
            return queryset.distinc()

        if user_id:
            queryset = queryset.filter(id=user_id)

        return queryset


class UserSearchDetailView(generics.RetrieveAPIView):
    serializer_class = UserSearchDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        User = get_user_model()
        queryset = User.objects.all()
        user_id = self.kwargs.get("pk", None)

        if user_id is not None:
            queryset = queryset.filter(id=user_id)

        return queryset


class SubscribeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, user_id):
        try:
            subscribed_user = get_user_model().objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if subscribed_user == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        subscription, created = Subscription.objects.get_or_create(
            subscriber=request.user, subscribed=subscribed_user
        )

        if not created:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


class SubscriberListView(generics.ListAPIView):
    serializer_class = SubscribersListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Subscription.objects.filter(subscribed=self.request.user)


class SubscribersDetailView(generics.RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscribersDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        subscription_id = self.kwargs.get("pk")
        subscription = Subscription.objects.get(
            id=subscription_id, subscribed=self.request.user
        )
        return subscription


class SubscriptionsListView(generics.ListAPIView):
    serializer_class = SubscriptionsListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)


class SubscriptionsDetailView(generics.RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionsDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        subscription_id = self.kwargs.get("pk")
        subscription = Subscription.objects.get(
            id=subscription_id, subscriber=self.request.user
        )
        return subscription
