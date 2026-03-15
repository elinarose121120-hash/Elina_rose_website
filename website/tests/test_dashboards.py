"""
Test cases for dashboard functionality
Tests admin and manager dashboard features
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import UserProfile, GalleryImage
from django.core.files.uploadedfile import SimpleUploadedFile


class AdminDashboardTests(TestCase):
    """Test admin dashboard functionality"""
    
    def setUp(self):
        """Set up test client and admin user"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        # Profile is auto-created, just update role
        self.admin.profile.role = 'admin'
        self.admin.profile.save()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        # Profile is auto-created, just update role
        self.user1.profile.role = 'user'
        self.user1.profile.save()
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        # Profile is auto-created, just update role
        self.user2.profile.role = 'user'
        self.user2.profile.save()
    
    def test_admin_dashboard_shows_all_users(self):
        """Test admin dashboard displays all users"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.context)
        # Should include all users
        users = response.context['users']
        self.assertIn(self.user1, users)
        self.assertIn(self.user2, users)
        self.assertIn(self.admin, users)
    
    def test_admin_can_promote_user_to_manager(self):
        """Test admin can promote user to manager"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('admin_dashboard'), {
            'user_id': self.user1.id,
            'action': 'change_role',
            'role': 'manager'
        })
        self.assertEqual(response.status_code, 302)  # Redirects
        # Check role was changed
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.profile.role, 'manager')
    
    def test_admin_can_change_user_to_admin(self):
        """Test admin can change user role to admin"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('admin_dashboard'), {
            'user_id': self.user1.id,
            'action': 'change_role',
            'role': 'admin'
        })
        self.assertEqual(response.status_code, 302)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.profile.role, 'admin')
    
    def test_admin_cannot_change_own_role(self):
        """Test admin cannot change their own role"""
        self.client.login(username='admin', password='adminpass123')
        initial_role = self.admin.profile.role
        response = self.client.post(reverse('admin_dashboard'), {
            'user_id': self.admin.id,
            'action': 'change_role',
            'role': 'user'
        })
        # Should redirect but role should not change
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.profile.role, initial_role)


class ManagerDashboardTests(TestCase):
    """Test manager dashboard functionality"""
    
    def setUp(self):
        """Set up test client and manager user"""
        self.client = Client()
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='managerpass123'
        )
        # Profile is auto-created, just update role
        self.manager.profile.role = 'manager'
        self.manager.profile.save()
    
    def test_manager_dashboard_displays_upload_form(self):
        """Test manager dashboard displays upload form"""
        self.client.login(username='manager', password='managerpass123')
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('recent_uploads', response.context)
    
    def test_manager_can_upload_image(self):
        """Test manager can upload image to gallery"""
        self.client.login(username='manager', password='managerpass123')
        
        # Create a simple image file
        image_content = b'fake image content'
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            image_content,
            content_type="image/jpeg"
        )
        
        initial_count = GalleryImage.objects.count()
        response = self.client.post(reverse('manager_dashboard'), {
            'content_type': 'image',
            'image': image_file,
            'title': 'Test Image',
            'description': 'Test description',
            'featured': False
        })
        
        self.assertEqual(response.status_code, 302)  # Redirects after upload
        self.assertEqual(GalleryImage.objects.count(), initial_count + 1)
        
        # Check the uploaded item
        uploaded_item = GalleryImage.objects.latest('created_at')
        self.assertEqual(uploaded_item.title, 'Test Image')
        self.assertEqual(uploaded_item.content_type, 'image')
        self.assertEqual(uploaded_item.uploaded_by, self.manager)
    
    def test_manager_can_upload_video(self):
        """Test manager can upload video to gallery"""
        self.client.login(username='manager', password='managerpass123')
        
        # Create a simple video file
        video_content = b'fake video content'
        video_file = SimpleUploadedFile(
            "test_video.mp4",
            video_content,
            content_type="video/mp4"
        )
        
        initial_count = GalleryImage.objects.count()
        response = self.client.post(reverse('manager_dashboard'), {
            'content_type': 'video',
            'video': video_file,
            'title': 'Test Video',
            'description': 'Test video description',
            'featured': 'on'  # Checkbox sends 'on' when checked
        }, format='multipart')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(GalleryImage.objects.count(), initial_count + 1)
        
        # Check the uploaded item
        uploaded_item = GalleryImage.objects.latest('created_at')
        self.assertEqual(uploaded_item.title, 'Test Video')
        self.assertEqual(uploaded_item.content_type, 'video')
        self.assertTrue(uploaded_item.featured)
    
    def test_manager_dashboard_shows_recent_uploads(self):
        """Test manager dashboard shows recent uploads"""
        self.client.login(username='manager', password='managerpass123')
        
        # Refresh manager to ensure profile exists
        self.manager.refresh_from_db()
        
        # Create some gallery items
        GalleryImage.objects.create(
            title='Upload 1',
            content_type='image',
            uploaded_by=self.manager
        )
        GalleryImage.objects.create(
            title='Upload 2',
            content_type='video',
            uploaded_by=self.manager
        )
        
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('recent_uploads', response.context)
        recent_uploads = response.context['recent_uploads']
        # Should show up to 10 recent uploads
        self.assertGreaterEqual(len(recent_uploads), 2)

