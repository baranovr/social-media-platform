from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from social_media.serializers import (
    SubscriberListSerializer,
    SubscriptionsListSerializer,
    PostDetailSerializer,
    SubscribedDetailSerializer,
    PostListSerializer
)

from social_media.models import Subscription, Post

from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    permission_classes = (permissions.AllowAny,)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user


class PostListView(generics.ListCreateAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class UserPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
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


class SubscribeView(APIView):
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


class SubscriberListView(APIView):
    def get(self, request):
        subscriptions = Subscription.objects.filter(subscribed=request.user)
        serializer = SubscriberListSerializer(subscriptions, many=True)
        return Response(serializer.data)


class SubscriptionsListView(APIView):
    def get(self, request):
        subscriptions = Subscription.objects.filter(subscriber=request.user)
        serializer = SubscriptionsListSerializer(subscriptions, many=True)
        return Response(serializer.data)


class UnsubscribeView(APIView):
    def delete(self, request, pk):
        try:
            subscription = Subscription.objects.get(
                subscriber=request.user, subscribed__id=pk
            )
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
