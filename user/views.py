from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class CreateTokenView(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = (permissions.IsAdminUser,)

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
