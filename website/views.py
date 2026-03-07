from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post, GalleryImage, ContactMessage


def home(request):
    featured_posts = Post.objects.filter(published=True)[:3]
    featured_gallery = GalleryImage.objects.filter(featured=True)[:6]
    return render(request, 'website/home.html', {
        'featured_posts': featured_posts,
        'featured_gallery': featured_gallery,
    })


def about(request):
    return render(request, 'website/about.html')


def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'website/gallery.html', {'images': images})


def blog(request):
    posts = Post.objects.filter(published=True)
    return render(request, 'website/blog.html', {'posts': posts})


def blog_detail(request, post_id):
    post = Post.objects.get(id=post_id, published=True)
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

