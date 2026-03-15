"""
Test cases for authentication and role-based access control
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import UserProfile


class AuthenticationTests(TestCase):
    """Test authentication functionality"""
    
    def setUp(self):
        """Set up test client and users"""
        self.client = Client()
        
        # Create regular user
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )
        # Profile is auto-created, just update role
        self.user.profile.role = 'user'
        self.user.profile.save()
        
        # Create manager user
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='managerpass123'
        )
        # Profile is auto-created, just update role
        self.manager.profile.role = 'manager'
        self.manager.profile.save()
        
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        # Profile is auto-created, just update role
        self.admin.profile.role = 'admin'
        self.admin.profile.save()
        
        # Create superuser
        self.superuser = User.objects.create_user(
            username='superuser',
            email='super@example.com',
            password='superpass123',
            is_superuser=True
        )
    
    def test_regular_user_cannot_access_admin_dashboard(self):
        """Test regular user cannot access admin dashboard"""
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects
    
    def test_regular_user_cannot_access_manager_dashboard(self):
        """Test regular user cannot access manager dashboard"""
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects
    
    def test_manager_can_access_manager_dashboard(self):
        """Test manager can access manager dashboard"""
        self.client.login(username='manager', password='managerpass123')
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_manager_cannot_access_admin_dashboard(self):
        """Test manager cannot access admin dashboard"""
        self.client.login(username='manager', password='managerpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects
    
    def test_admin_can_access_admin_dashboard(self):
        """Test admin can access admin dashboard"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_access_manager_dashboard(self):
        """Test admin can access manager dashboard"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_superuser_can_access_admin_dashboard(self):
        """Test superuser can access admin dashboard"""
        self.client.login(username='superuser', password='superpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_superuser_can_access_manager_dashboard(self):
        """Test superuser can access manager dashboard"""
        self.client.login(username='superuser', password='superpass123')
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_superuser_gets_profile_created(self):
        """Test superuser gets profile created automatically"""
        self.client.login(username='superuser', password='superpass123')
        # Access dashboard to trigger profile creation
        self.client.get(reverse('admin_dashboard'))
        # Refresh from database
        self.superuser.refresh_from_db()
        # Check profile was created
        self.assertTrue(hasattr(self.superuser, 'profile'))
        self.assertEqual(self.superuser.profile.role, 'admin')
    
    def test_logout_redirects(self):
        """Test logout redirects properly"""
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects

