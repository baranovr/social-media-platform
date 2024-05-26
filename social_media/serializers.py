from rest_framework import serializers

from social_media.models import (
    Hashtag,
    Post,
    Comment,
    Like,
    Dislike,
    Subscription
)


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("id", "name",)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "photo",
            "title",
            "content",
            "hashtags",
            "date_posted",
        )


class PostListSerializer(PostSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "user", "title", "date_posted",)


class SubscribedPostListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username", read_only=True
    )

    class Meta:
        model = Post
        fields = ("id", "username", "title", "content", "date_posted",)
        read_only_fields = ["username"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "content", "created_at", "updated_at")


class CommentListSerializer(CommentSerializer):
    post_title = serializers.CharField(source="post.title", read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = Comment
        fields = ("id", "post_title", "user", "created_at",)
        read_only_fields = ("created_at",)


class CommentDetailSerializer(CommentSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "user_email",
            "post_title",
            "content",
            "created_at",
            "updated_at"
        )
        read_only_fields = ("created_at", "updated_at",)


class CommentInPostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "user", "content", "created_at", "updated_at",)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "post")


class LikeListSerializer(LikeSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)
    post_id = serializers.IntegerField(source="post.id", read_only=True)
    
    class Meta:
        model = Like
        fields = ("id", "user", "post_id", "post_title")


class LikeDetailSerializer(LikeSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ("id", "user", "post")


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ("id", "post")


class DislikeListSerializer(DislikeSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)
    post_id = serializers.IntegerField(source="post.id", read_only=True)

    class Meta:
        model = Like
        fields = ("id", "user", "post_id", "post_title")


class DislikeDetailSerializer(DislikeSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Dislike
        fields = ("id", "user", "post")


class PostDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    hashtags = HashtagSerializer(many=True, read_only=True)

    def get_likes_count(self, obj):
        return Like.objects.filter(post=obj).count()

    def get_dislikes_count(self, obj):
        return Dislike.objects.filter(post=obj).count()

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentInPostSerializer(comments, many=True).data

    class Meta:
        model = Post
        fields = (
            "id",
            "username",
            "user_email",
            "photo",
            "title",
            "content",
            "hashtags",
            "date_posted",
            "likes_count",
            "dislikes_count",
            "comments",
        )


class SubscribedPostDetailSerializer(PostDetailSerializer):

    class Meta:
        model = Post
        fields = (
            "id",
            "username",
            "user_email",
            "photo",
            "title",
            "content",
            "hashtags",
            "date_posted",
            "likes_count",
            "dislikes_count",
            "comments",
            )
        read_only_fields = ("username", "user_email")


class LikedPostSerializer(PostDetailSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "username",
            "photo",
            "title",
            "content",
            "hashtags",
            "date_posted",
        )


class DislikedPostSerializer(PostDetailSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "username",
            "photo",
            "title",
            "content",
            "hashtags",
            "date_posted",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = serializers.CharField(
        source="subscriber.username", read_only=True
    )
    subscribed = serializers.CharField(
        source="subscribed.username", read_only=True
    )

    class Meta:
        model = Subscription
        fields = ("id", "subscriber", "subscribed", "created_at")
        read_only_fields = ("created_at",)


class SubscriptionsListSerializer(SubscriptionSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "subscribed")


class SubscriptionsDetailSerializer(SubscriptionSerializer):
    avatar = serializers.CharField(
        source="subscribed.avatar", read_only=True,
    )
    username = serializers.CharField(
        source="subscribed.username", read_only=True
    )
    email = serializers.CharField(
        source="subscribed.email", read_only=True
    )
    full_name = serializers.CharField(
        source="subscribed.full_name", read_only=True
    )
    about_user = serializers.CharField(
        source="subscribed.about_me", read_only=True
    )

    class Meta:
        model = Subscription
        fields = (
            "id", "avatar", "username", "full_name", "email", "about_user"
        )
        read_only_fields = ("id", "created_at")


class SubscribersListSerializer(SubscriptionSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "subscriber")


class SubscribersDetailSerializer(SubscriptionSerializer):
    avatar = serializers.CharField(
        source="subscriber.avatar", read_only=True,
    )
    username = serializers.CharField(
        source="subscriber.username", read_only=True
    )
    email = serializers.CharField(
        source="subscriber.email", read_only=True
    )
    full_name = serializers.CharField(
        source="subscriber.full_name", read_only=True
    )
    about_user = serializers.CharField(
        source="subscriber.about_me", read_only=True
    )

    class Meta:
        model = Subscription
        fields = (
            "id", "avatar", "username", "full_name", "email", "about_user"
        )
        read_only_fields = ("id", "created_at")
