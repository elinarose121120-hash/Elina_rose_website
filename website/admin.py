from django.contrib import admin
from .models import Post, GalleryImage, ContactMessage


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

