from rest_framework import serializers

from django.contrib.auth import get_user_model

from social_media.models import Post, Subscription


class UserSerializer(serializers.ModelSerializer):
    subscribers = serializers.SerializerMethodField()
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "is_staff",
            "about_me",
            "password",
            "date_joined",
            "subscribers",
            "subscriptions"
        )
        read_only_fields = ("date_joined", "subscribers", "subscriptions",)
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
                "min_length": 8,
            }
        }

    def get_subscribers(self, obj):
        return Subscription.objects.filter(subscribed=obj).count()

    def get_subscriptions(self, obj):
        return Subscription.objects.filter(subscriber=obj).count()

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = get_user_model().objects.create_user(
            password=password, **validated_data
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class UserListSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    def get_posts_count(self, obj):
        return Post.objects.filter(user=obj).count()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "full_name",
            "email",
            "posts_count",
            "is_staff",
            "date_joined"
        )


class UserDetailSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "is_staff",
            "about_me",
            "date_joined",
            "subscribers",
            "subscriptions",
            "posts"
        )
        read_only_fields = ("is_staff", "date_joined")
