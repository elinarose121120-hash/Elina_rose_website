"""
URL configuration for elina_rose_website project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from website import views as website_views

# Customize admin site
admin.site.site_header = "Elina Rose Admin"
admin.site.site_title = "Elina Rose Admin Portal"
admin.site.index_title = "Welcome to Elina Rose Administration"

urlpatterns = [
    # Custom dashboard URLs - must come BEFORE Django admin to avoid conflicts
    path('admin/dashboard/', website_views.admin_dashboard, name='admin_dashboard'),
    path('manager/dashboard/', website_views.manager_dashboard, name='manager_dashboard'),
    # Django admin (catches remaining /admin/* URLs)
    path('admin/', admin.site.urls),
    # All other website URLs
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

