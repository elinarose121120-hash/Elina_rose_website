from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Post, GalleryImage, ContactMessage, UserProfile
from .decorators import admin_required, manager_required


def home(request):
    featured_posts = Post.objects.filter(published=True)[:3]
    # Filter featured gallery items that have images (for homepage preview)
    # Only get items with content_type='image' and that actually have an image file
    featured_gallery = [
        item for item in GalleryImage.objects.filter(featured=True, content_type='image')[:6]
        if item.image  # Only include items that have an image file
    ]
    return render(request, 'website/home.html', {
        'featured_posts': featured_posts,
        'featured_gallery': featured_gallery,
    })


def about(request):
    return render(request, 'website/about.html')


def gallery(request):
    gallery_items = GalleryImage.objects.all()
    return render(request, 'website/gallery.html', {'gallery_items': gallery_items})


def blog(request):
    posts = Post.objects.filter(published=True)
    return render(request, 'website/blog.html', {'posts': posts})


def blog_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id, published=True)
    except Post.DoesNotExist:
        from django.http import Http404
        raise Http404("Post not found")
    recent_posts = Post.objects.filter(published=True).exclude(id=post_id)[:3]
    return render(request, 'website/blog_detail.html', {
        'post': post,
        'recent_posts': recent_posts,
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Thank you for your message! I\'ll get back to you soon.')
        return redirect('contact')
    
    return render(request, 'website/contact.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'website/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not username or not email or not password:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'website/signup.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'website/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'website/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email or try logging in.')
            return render(request, 'website/signup.html')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created successfully.')
            return redirect('home')
        except Exception as e:
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            return render(request, 'website/signup.html')
    
    return render(request, 'website/signup.html')


@admin_required
def admin_dashboard(request):
    users = User.objects.all().select_related('profile')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        new_role = request.POST.get('role')
        
        user = get_object_or_404(User, id=user_id)
        
        # Prevent admin from changing their own role
        if user.id == request.user.id and action == 'change_role':
            messages.error(request, 'You cannot change your own role.')
            return redirect('admin_dashboard')
        
        if action == 'make_manager':
            if hasattr(user, 'profile'):
                user.profile.role = 'manager'
                user.profile.save()
                messages.success(request, f'{user.username} has been promoted to Manager.')
            else:
                UserProfile.objects.create(user=user, role='manager')
                messages.success(request, f'{user.username} has been promoted to Manager.')
        elif action == 'change_role' and new_role:
            if hasattr(user, 'profile'):
                user.profile.role = new_role
                user.profile.save()
                messages.success(request, f'{user.username}\'s role has been changed to {new_role.capitalize()}.')
            else:
                UserProfile.objects.create(user=user, role=new_role)
                messages.success(request, f'{user.username}\'s role has been set to {new_role.capitalize()}.')
        
        return redirect('admin_dashboard')
    
    return render(request, 'website/admin_dashboard.html', {'users': users})


@manager_required
def manager_dashboard(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        featured = request.POST.get('featured') == 'on'
        content_type = request.POST.get('content_type', 'image')
        
        gallery_item = GalleryImage(
            title=title,
            description=description,
            featured=featured,
            content_type=content_type,
            uploaded_by=request.user
        )
        
        if content_type == 'image':
            if 'image' in request.FILES:
                gallery_item.image = request.FILES['image']
            else:
                messages.error(request, 'Please select an image file.')
                return redirect('manager_dashboard')
        elif content_type == 'video':
            if 'video' in request.FILES:
                gallery_item.video = request.FILES['video']
            else:
                messages.error(request, 'Please select a video file.')
                return redirect('manager_dashboard')
        
        gallery_item.save()
        messages.success(request, f'{content_type.capitalize()} uploaded successfully!')
        return redirect('manager_dashboard')
    
    # Get recent uploads by this manager
    recent_uploads = GalleryImage.objects.filter(uploaded_by=request.user)[:10]
    return render(request, 'website/manager_dashboard.html', {'recent_uploads': recent_uploads})

