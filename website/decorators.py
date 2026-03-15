from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import UserProfile


def admin_required(view_func):
    """Decorator to check if user is admin or superuser"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        
        # Check if user is Django superuser (has full admin access)
        if request.user.is_superuser:
            # Ensure superuser has a profile with admin role
            if not hasattr(request.user, 'profile'):
                UserProfile.objects.create(user=request.user, role='admin')
            elif request.user.profile.role != 'admin':
                request.user.profile.role = 'admin'
                request.user.profile.save()
            return view_func(request, *args, **kwargs)
        
        # Check if user has profile with admin role
        if not hasattr(request.user, 'profile'):
            messages.error(request, 'User profile not found. Please contact an administrator.')
            return redirect('home')
        
        if request.user.profile.role != 'admin':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def manager_required(view_func):
    """Decorator to check if user is manager, admin, or superuser"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        
        # Check if user is Django superuser (has full admin access)
        if request.user.is_superuser:
            # Ensure superuser has a profile with admin role
            if not hasattr(request.user, 'profile'):
                UserProfile.objects.create(user=request.user, role='admin')
            elif request.user.profile.role != 'admin':
                request.user.profile.role = 'admin'
                request.user.profile.save()
            return view_func(request, *args, **kwargs)
        
        # Check if user has profile with manager or admin role
        if not hasattr(request.user, 'profile'):
            messages.error(request, 'User profile not found. Please contact an administrator.')
            return redirect('home')
        
        if request.user.profile.role not in ['manager', 'admin']:
            messages.error(request, 'Access denied. Manager or Admin privileges required.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

