"""
URL configuration for elina_rose_website project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "Elina Rose Admin"
admin.site.site_title = "Elina Rose Admin Portal"
admin.site.index_title = "Welcome to Elina Rose Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

