"""
Test cases for website views
Tests view functionality, context data, and edge cases
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import UserProfile, Post, GalleryImage, ContactMessage
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class ViewTests(TestCase):
    """Test website views"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test post
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content for blog post',
            published=True
        )
        
        # Create test gallery image (without actual file to test edge cases)
        self.gallery_item = GalleryImage.objects.create(
            title='Test Image',
            description='Test description',
            content_type='image',
            featured=True
        )
    
    def test_home_view_returns_published_posts(self):
        """Test home view returns published posts"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('featured_posts', response.context)
    
    def test_home_view_handles_gallery_without_images(self):
        """Test home view handles gallery items without images gracefully"""
        # Create gallery item without image
        GalleryImage.objects.create(
            title='Video Item',
            content_type='video',
            featured=True
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Should not raise ValueError
    
    def test_gallery_view_returns_all_items(self):
        """Test gallery view returns all gallery items"""
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('gallery_items', response.context)
    
    def test_blog_view_returns_published_posts_only(self):
        """Test blog view returns only published posts"""
        unpublished_post = Post.objects.create(
            title='Unpublished',
            content='Content',
            published=False
        )
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('posts', response.context)
        # Unpublished post should not be in context
        posts = response.context['posts']
        self.assertNotIn(unpublished_post, posts)
    
    def test_blog_detail_view_returns_post(self):
        """Test blog detail view returns correct post"""
        response = self.client.get(reverse('blog_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)
    
    def test_contact_view_get(self):
        """Test contact view GET request"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
    
    def test_contact_view_post(self):
        """Test contact view POST request creates message"""
        initial_count = ContactMessage.objects.count()
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after POST
        self.assertEqual(ContactMessage.objects.count(), initial_count + 1)
    
    def test_login_view_get(self):
        """Test login view GET request"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_post_valid_credentials(self):
        """Test login view POST with valid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after login
    
    def test_login_view_post_invalid_credentials(self):
        """Test login view POST with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stays on login page
        # Should have error message
    
    def test_signup_view_get(self):
        """Test signup view GET request"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_signup_view_post_valid_data(self):
        """Test signup view POST with valid data"""
        initial_count = User.objects.count()
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after signup
        self.assertEqual(User.objects.count(), initial_count + 1)
    
    def test_signup_view_post_password_mismatch(self):
        """Test signup view POST with password mismatch"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'differentpass'
        })
        self.assertEqual(response.status_code, 200)  # Stays on signup page
        # Should have error message
    
    def test_signup_view_post_duplicate_username(self):
        """Test signup view POST with duplicate username"""
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',  # Already exists
            'email': 'newemail@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        })
        self.assertEqual(response.status_code, 200)  # Stays on signup page
        # Should have error message

