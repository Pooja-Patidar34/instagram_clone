from django.contrib import admin
from .models import Profile,Post,Like,Comment,Follow,Story,Notification

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Story)
admin.site.register(Notification)