from django.contrib import admin

# Register your models here.

from . models import Robot
admin.site.register(Robot)

from . models import Goal
admin.site.register(Goal)

from . models import Post
admin.site.register(Post)