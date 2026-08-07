from django.contrib import admin
from .models import Tweet, Profile, Follow, Like

admin.site.register(Tweet)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Like)