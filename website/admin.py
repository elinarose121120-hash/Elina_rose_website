from django.contrib import admin
from .models import Post, GalleryImage, ContactMessage, UserProfile, GalleryLike, GalleryComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'published']
    list_filter = ['published', 'created_at']
    search_fields = ['title', 'content']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'featured']
    list_filter = ['featured', 'created_at']
    search_fields = ['title', 'description']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'read']
    list_filter = ['read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']


@admin.register(GalleryLike)
class GalleryLikeAdmin(admin.ModelAdmin):
    list_display = ['gallery_item', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'gallery_item__title']
    readonly_fields = ['created_at']


@admin.register(GalleryComment)
class GalleryCommentAdmin(admin.ModelAdmin):
    list_display = ['gallery_item', 'user', 'created_at', 'text_preview']
    list_filter = ['created_at']
    search_fields = ['user__username', 'gallery_item__title', 'text']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'

