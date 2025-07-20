from django.contrib import admin
from test_django.models import Category, Post, Comment, Notificated, Profile
from test_django.chat_models import ChatGroup, GroupMessage

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "watched", "is_published", "category_id", "create_at", "update_at")
    list_display_links = ("id", "title")
    list_editable = ("is_published",)
    readonly_fields = ("watched",)
    list_filter = ("id", "is_published", "category_id", "update_at")


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
admin.site.register(Notificated)
admin.site.register(Profile)
