from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from social_media.tests.test_social_media_serializers import BaseTestCase

from social_media.models import (
    Hashtag,
    Post,
    Comment,
    Subscription
)

User = get_user_model()


class HashtagModelTest(BaseTestCase):
    def test_hashtag_str(self):
        hashtag = Hashtag.objects.create(name="Test")

        self.assertEqual(str(hashtag), "Test")


class PostModelTest(BaseTestCase):
    def test_post_str(self):
        post = Post.objects.create(
            user=self.user, title="Test Post", content="Test content"
        )

        self.assertEqual(
            str(post), f"{post.title} - {post.date_posted}"
        )

    def test_post_hashtags(self):
        post = Post.objects.create(
            user=self.user, title="Test Post", content="Test content"
        )
        post.hashtags.add(self.hashtag)

        self.assertIn(self.hashtag, post.hashtags.all())

    def test_post_photo_upload(self):
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test content",
            photo=image
        )

        self.assertTrue(post.photo)


class CommentModelTest(BaseTestCase):
    def test_comment_str(self):
        comment = Comment.objects.create(
            post=self.post, user=self.user, content="Test comment"
        )

        self.assertEqual(
            str(comment), f"{comment.user}: {comment.content}"
        )


class SubscriptionModelTest(TestCase):
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

    def test_subscription_str(self):
        subscription = Subscription.objects.create(
            subscriber=self.user1, subscribed=self.user2
        )

        self.assertEqual(
            str(subscription),
            f"{subscription.subscriber} "
            f"is subscribed on {subscription.subscribed}"
        )

    def test_subscription_unique_together(self):
        subscription = Subscription.objects.create(
            subscriber=self.user1, subscribed=self.user2
        )

        with self.assertRaises(Exception):
            Subscription.objects.create(
                subscriber=self.user1, subscribed=self.user2
            )
