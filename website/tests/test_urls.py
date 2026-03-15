"""
Test cases for all website URLs
This ensures all URLs are accessible and return correct status codes
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import UserProfile, Post, GalleryImage, ContactMessage


class URLTests(TestCase):
    """Test all website URLs"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Profile is auto-created, just update role
        self.user.profile.role = 'user'
        self.user.profile.save()
        
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        # Profile is auto-created, just update role
        self.admin_user.profile.role = 'admin'
        self.admin_user.profile.save()
        
        self.manager_user = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='managerpass123'
        )
        # Profile is auto-created, just update role
        self.manager_user.profile.role = 'manager'
        self.manager_user.profile.save()
    
    def test_home_url(self):
        """Test home page URL"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Elina Rose')
    
    def test_about_url(self):
        """Test about page URL"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
    
    def test_gallery_url(self):
        """Test gallery page URL"""
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
    
    def test_blog_url(self):
        """Test blog listing page URL"""
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
    
    def test_contact_url(self):
        """Test contact page URL"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_url(self):
        """Test login page URL"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_signup_url(self):
        """Test signup page URL"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_logout_url_redirects_when_not_logged_in(self):
        """Test logout URL redirects when user is not logged in"""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_admin_dashboard_url_requires_authentication(self):
        """Test admin dashboard requires authentication"""
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_admin_dashboard_url_requires_admin_role(self):
        """Test admin dashboard requires admin role"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects to home
    
    def test_admin_dashboard_url_allows_admin_access(self):
        """Test admin dashboard allows admin access"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_manager_dashboard_url_requires_authentication(self):
        """Test manager dashboard requires authentication"""
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_manager_dashboard_url_requires_manager_role(self):
        """Test manager dashboard requires manager or admin role"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects to home
    
    def test_manager_dashboard_url_allows_manager_access(self):
        """Test manager dashboard allows manager access"""
        self.client.login(username='manager', password='managerpass123')
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_manager_dashboard_url_allows_admin_access(self):
        """Test manager dashboard allows admin access"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_blog_detail_url_with_valid_post(self):
        """Test blog detail URL with valid post"""
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            published=True
        )
        response = self.client.get(reverse('blog_detail', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_blog_detail_url_with_invalid_post(self):
        """Test blog detail URL with invalid post ID"""
        response = self.client.get(reverse('blog_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

