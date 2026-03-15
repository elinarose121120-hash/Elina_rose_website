"""
Test cases for models
Tests model creation, relationships, and methods
"""
from django.test import TestCase
from django.contrib.auth.models import User
from website.models import UserProfile, Post, GalleryImage, ContactMessage
from django.utils import timezone


class ModelTests(TestCase):
    """Test website models"""
    
    def test_user_profile_created_on_user_creation(self):
        """Test UserProfile is created when User is created"""
        # Get current user count to determine if this is first user
        user_count_before = User.objects.count()
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Refresh from database to ensure signal has processed
        user.refresh_from_db()
        # Profile should be created automatically
        self.assertTrue(hasattr(user, 'profile'))
        # First user becomes admin, others become user
        expected_role = 'admin' if user_count_before == 0 else 'user'
        self.assertEqual(user.profile.role, expected_role)
    
    def test_first_user_becomes_admin(self):
        """Test first user automatically becomes admin"""
        user = User.objects.create_user(
            username='firstuser',
            email='first@example.com',
            password='testpass123'
        )
        self.assertEqual(user.profile.role, 'admin')
    
    def test_post_model_creation(self):
        """Test Post model creation"""
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            published=True
        )
        self.assertEqual(str(post), 'Test Post')
        self.assertTrue(post.published)
        self.assertIsNotNone(post.created_at)
    
    def test_gallery_image_model_creation(self):
        """Test GalleryImage model creation"""
        gallery_item = GalleryImage.objects.create(
            title='Test Image',
            description='Test description',
            content_type='image',
            featured=True
        )
        self.assertEqual(str(gallery_item), 'Test Image')
        self.assertEqual(gallery_item.content_type, 'image')
        self.assertTrue(gallery_item.featured)
    
    def test_gallery_video_model_creation(self):
        """Test GalleryImage model with video"""
        gallery_item = GalleryImage.objects.create(
            title='Test Video',
            content_type='video',
            featured=False
        )
        self.assertEqual(gallery_item.content_type, 'video')
        self.assertFalse(gallery_item.featured)
    
    def test_contact_message_model_creation(self):
        """Test ContactMessage model creation"""
        message = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='Test message'
        )
        self.assertEqual(str(message), 'Test User - Test Subject')
        self.assertFalse(message.read)
        self.assertIsNotNone(message.created_at)
    
    def test_user_profile_role_methods(self):
        """Test UserProfile role helper methods"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Test is_user
        user.profile.role = 'user'
        user.profile.save()
        self.assertTrue(user.profile.is_user())
        self.assertFalse(user.profile.is_manager())
        self.assertFalse(user.profile.is_admin())
        
        # Test is_manager
        user.profile.role = 'manager'
        user.profile.save()
        self.assertTrue(user.profile.is_manager())
        self.assertFalse(user.profile.is_user())
        self.assertFalse(user.profile.is_admin())
        
        # Test is_admin
        user.profile.role = 'admin'
        user.profile.save()
        self.assertTrue(user.profile.is_admin())
        self.assertFalse(user.profile.is_user())
        self.assertFalse(user.profile.is_manager())

