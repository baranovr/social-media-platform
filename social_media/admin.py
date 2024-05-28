from django.contrib import admin

from social_media.models import Post, Comment, Like, Dislike, Subscription


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Subscription)
