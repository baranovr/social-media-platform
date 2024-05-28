from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from social_media.models import (
    Hashtag,
    Post,
    Comment,
    Like,
    Dislike,
    Subscription
)
from social_media.serializers import (
    HashtagSerializer,
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
    DislikeSerializer,
    SubscriptionSerializer,
)

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="otherpass"
        )
        self.hashtag = Hashtag.objects.create(name="Test")
        self.post = Post.objects.create(
            user=self.user, title="Test Post", content="Test content"
        )
        self.post.hashtags.add(self.hashtag)
        self.comment = Comment.objects.create(
            post=self.post, user=self.user, content="Test comment"
        )
        self.like = Like.objects.create(user=self.user, post=self.post)
        self.dislike = Dislike.objects.create(
            user=self.other_user, post=self.post
        )
        self.subscription = Subscription.objects.create(
            subscriber=self.user, subscribed=self.other_user
        )


class HashtagSerializerTest(TestCase):
    def test_hashtag_serializer(self):
        hashtag = Hashtag.objects.create(name="Test")
        serializer = HashtagSerializer(hashtag)

        self.assertEqual(
            serializer.data, {"id": hashtag.id, "name": "Test"}
        )


class PostSerializerTest(BaseTestCase):
    def test_post_serializer(self):
        post = Post.objects.create(
            user=self.user, title="Test Post", content="Test content"
        )
        post.hashtags.add(self.hashtag)
        serializer = PostSerializer(post)

        self.assertEqual(
            serializer.data,
            {
                "id": post.id,
                "photo": None,
                "title": "Test Post",
                "content": "Test content",
                "hashtags": [self.hashtag.id],
                "date_posted": post.date_posted.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            }
        )


class CommentSerializerTest(BaseTestCase):
    def test_comment_serializer(self):
        comment = Comment.objects.create(
            post=self.post, user=self.user, content="Test comment"
        )
        serializer = CommentSerializer(comment)

        self.assertEqual(
            serializer.data,
            {
                "id": comment.id,
                "post": comment.post.id,
                "content": "Test comment",
                "created_at": comment.created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "updated_at": comment.updated_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            }
        )


class LikeSerializerTest(BaseTestCase):
    def test_like_serializer(self):
        other_post = Post.objects.create(
            user=self.user, title="Other Post", content="Other content"
        )
        like = Like.objects.create(user=self.user, post=other_post)
        serializer = LikeSerializer(like)

        self.assertEqual(
            serializer.data, {"id": like.id, "post": like.post.id}
        )


class DislikeSerializerTest(BaseTestCase):
    def test_dislike_serializer(self):
        dislike = Dislike.objects.create(user=self.user, post=self.post)
        serializer = DislikeSerializer(dislike)

        self.assertEqual(
            serializer.data,
            {"id": dislike.id, "post": dislike.post.id}
        )


class SubscriptionSerializerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="test1@example.com",
            password="testpass1"
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpass2"
        )

    def test_subscription_serializer(self):
        subscription = Subscription.objects.create(
            subscriber=self.user1, subscribed=self.user2
        )
        serializer = SubscriptionSerializer(subscription)

        self.assertEqual(
            serializer.data,
            {
                "id": subscription.id,
                "subscriber": subscription.subscriber.username,
                "subscribed": subscription.subscribed.username,
                "created_at": subscription.created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            }
        )
