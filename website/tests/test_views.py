"""
Test cases for website views
Tests view functionality, context data, and edge cases
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import UserProfile, Post, GalleryImage, ContactMessage, GalleryLike, GalleryComment
from django.core.files.uploadedfile import SimpleUploadedFile
import json
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
        """Test home view returns latest images and featured gallery"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('latest_images', response.context)
        self.assertIn('featured_gallery', response.context)
    
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
    
    def test_gallery_view_includes_like_comment_counts(self):
        """Test gallery view includes like and comment counts"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        # Check that gallery items have like_count and comment_count attributes
        gallery_items = response.context['gallery_items']
        for item in gallery_items:
            self.assertTrue(hasattr(item, 'like_count'))
            self.assertTrue(hasattr(item, 'comment_count'))
            self.assertTrue(hasattr(item, 'is_liked'))
    
    def test_toggle_like_creates_like(self):
        """Test toggle like creates a like"""
        self.client.login(username='testuser', password='testpass123')
        gallery_item = GalleryImage.objects.create(
            title='Test Image',
            content_type='image'
        )
        response = self.client.post(reverse('toggle_like', args=[gallery_item.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['is_liked'])
        self.assertEqual(data['like_count'], 1)
        self.assertTrue(GalleryLike.objects.filter(gallery_item=gallery_item, user=self.user).exists())
    
    def test_toggle_like_removes_like(self):
        """Test toggle like removes existing like"""
        self.client.login(username='testuser', password='testpass123')
        gallery_item = GalleryImage.objects.create(
            title='Test Image',
            content_type='image'
        )
        # Create a like first
        GalleryLike.objects.create(gallery_item=gallery_item, user=self.user)
        response = self.client.post(reverse('toggle_like', args=[gallery_item.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertFalse(data['is_liked'])
        self.assertEqual(data['like_count'], 0)
        self.assertFalse(GalleryLike.objects.filter(gallery_item=gallery_item, user=self.user).exists())
    
    def test_toggle_like_invalid_item(self):
        """Test toggle like with invalid item ID"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('toggle_like', args=[99999]))
        self.assertEqual(response.status_code, 404)
    
    def test_add_comment_creates_comment(self):
        """Test add comment creates a comment"""
        self.client.login(username='testuser', password='testpass123')
        gallery_item = GalleryImage.objects.create(
            title='Test Image',
            content_type='image'
        )
        response = self.client.post(reverse('add_comment', args=[gallery_item.id]), {
            'text': 'This is a test comment'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['comment_count'], 1)
        self.assertTrue(GalleryComment.objects.filter(gallery_item=gallery_item, user=self.user).exists())
    
    def test_add_comment_empty_text(self):
        """Test add comment with empty text returns error"""
        self.client.login(username='testuser', password='testpass123')
        gallery_item = GalleryImage.objects.create(
            title='Test Image',
            content_type='image'
        )
        response = self.client.post(reverse('add_comment', args=[gallery_item.id]), {
            'text': ''
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_add_comment_invalid_item(self):
        """Test add comment with invalid item ID"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_comment', args=[99999]), {
            'text': 'Test comment'
        })
        self.assertEqual(response.status_code, 404)
    
    def test_get_comments_returns_comments(self):
        """Test get comments returns comment list"""
        gallery_item = GalleryImage.objects.create(
            title='Test Image',
            content_type='image'
        )
        # Create some comments
        comment1 = GalleryComment.objects.create(
            gallery_item=gallery_item,
            user=self.user,
            text='First comment'
        )
        comment2 = GalleryComment.objects.create(
            gallery_item=gallery_item,
            user=self.user,
            text='Second comment'
        )
        response = self.client.get(reverse('get_comments', args=[gallery_item.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['comments']), 2)
        self.assertEqual(data['comment_count'], 2)
    
    def test_get_comments_invalid_item(self):
        """Test get comments with invalid item ID"""
        response = self.client.get(reverse('get_comments', args=[99999]))
        self.assertEqual(response.status_code, 404)

