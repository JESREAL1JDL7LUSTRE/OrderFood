from django.contrib import admin
from .models import PostedContent, Comment, Share, Reaction

# Register your models here.
@admin.register(PostedContent)
class PostedContentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "created_at", "updated_at")
    search_fields = ("user__email", "content")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "posted_content", "content", "parent_comment", "created_at")
    search_fields = ("user__email", "content", "posted_content__content")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "posted_content", "created_at")
    search_fields = ("user__email", "posted_content__content")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "posted_content", "type", "created_at")
    search_fields = ("user__email", "posted_content__content")
    list_filter = ("type", "created_at")
    ordering = ("-created_at",)
