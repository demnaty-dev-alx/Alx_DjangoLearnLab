from django.contrib import admin
from .models import Profile, Post, Comment, Tag

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
