from rest_framework import serializers

from social_media.models import Post, Comment, Like, Dislike


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "user", "title", "content", "date_posted",)


class PostListSerializer(PostSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = Post
        fields = ("id", "user", "title", "date_posted",)


class PostDetailSerializer(PostSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    
    class Meta:
        model = Post
        fields = (
            "id", "user", "user_email", "title", "content", "date_posted",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "user", "post", "content", "created_at", "updated_at")


class CommentListSerializer(CommentSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    comment_id = serializers.IntegerField(source="id", read_only=True)
    
    class Meta:
        model = Comment
        fields = ("id", "post", "user", "comment_id", "created_at",)
        read_only_fields = ("created_at",)


class CommentDetailSerializer(CommentSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            "id", "user", "user_email", "content", "created_at", "updated_at"
        )
        read_only_fields = ("created_at", "updated_at",)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "user", "post")


class LikeListSerializer(LikeSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post_title = serializers.IntegerField(source="post.title", read_only=True)
    
    class Meta:
        model = Like
        fields = ("id", "user", "post_title")


class LikeDetailSerializer(LikeSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post = PostSerializer(source="post", read_only=True)

    class Meta:
        model = Like
        fields = ("id", "user", "post")


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ("id", "user", "post")


class DislikeListSerializer(DislikeSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post_title = serializers.IntegerField(source="post.title", read_only=True)

    class Meta:
        model = Like
        fields = ("id", "user", "post_title")


class DislikeDetailSerializer(DislikeSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post = PostSerializer(source="post", read_only=True)

    class Meta:
        model = Dislike
        fields = ("id", "user", "post")
