import os
import uuid

from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db import models

from social_media_platform import settings


def post_photo_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/posts_photos/", filename)


class Post(models.Model):
    photo = models.ImageField(
        upload_to=post_photo_path, blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user}: {self.content}"


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "post"),)
        ordering = ["-user"]

    def __str__(self):
        return f"{self.user} - {self.post}"


class Dislike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "post"),)
        ordering = ["-user"]

    def __str__(self):
        return f"{self.user} - {self.post}"


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="subscriber"
    )
    subscribed = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="subscribed"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("subscriber", "subscribed"),)
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subscriber} is subscribed on {self.subscribed}"
