from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Gallery interactions
    path('gallery/<int:item_id>/like/', views.toggle_like, name='toggle_like'),
    path('gallery/<int:item_id>/comment/', views.add_comment, name='add_comment'),
    path('gallery/<int:item_id>/comments/', views.get_comments, name='get_comments'),
    # Note: Dashboard URLs are registered in main urls.py (elina_rose_website/urls.py)
    # to avoid conflicts with Django admin
]

