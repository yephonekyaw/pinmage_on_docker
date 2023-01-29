from django.contrib import admin
from .models import Pin, Comment

@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'pin', 'created']
    list_filter = ['created']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'pin', 'body']



