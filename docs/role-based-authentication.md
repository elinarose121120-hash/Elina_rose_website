# Role-Based Authentication System

## Overview
The Elina Rose website implements a three-tier role-based authentication system with Admin, Manager, and User levels. Each role has specific permissions and access to different features of the website.

## User Roles

### 1. Admin
- **Access**: Full system access
- **Permissions**:
  - Access Admin Dashboard
  - View all users
  - Promote users to Manager role
  - All Manager permissions

### 2. Manager
- **Access**: Content management
- **Permissions**:
  - Access Manager Dashboard
  - Upload images and videos to gallery
  - Manage gallery content
  - View own uploads

### 3. User
- **Access**: Standard website access
- **Permissions**:
  - View website content
  - Create account and login
  - No dashboard access

## Implementation

### UserProfile Model
Location: `website/models.py`

The `UserProfile` model extends Django's User model with role information:

```python
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(default=timezone.now)
```

**Key Features**:
- Automatically created when a User is created (via Django signals)
- First user automatically becomes Admin
- Helper methods: `is_admin()`, `is_manager()`, `is_user()`

### Access Control Decorators
Location: `website/decorators.py`

#### `@admin_required`
- Restricts access to Admin users only
- Redirects non-admin users with error message

#### `@manager_required`
- Restricts access to Manager and Admin users
- Redirects regular users with error message

### Admin Dashboard
Location: `website/templates/website/admin_dashboard.html`
URL: `/admin/dashboard/`

**Features**:
- List of all users with their roles
- User management table showing:
  - Username
  - Email
  - Role (with color-coded badges)
  - Date joined
  - Actions (promote to Manager)
- Ability to promote any user to Manager role
- Only accessible to Admin users

**View Function**: `admin_dashboard(request)`
- Uses `@admin_required` decorator
- Handles POST requests to change user roles
- Supports changing roles to User, Manager, or Admin
- Prevents admins from changing their own role
- Displays all users with their profiles

### Manager Dashboard
Location: `website/templates/website/manager_dashboard.html`
URL: `/manager/dashboard/`

**Features**:
- Content upload form supporting:
  - Images (JPG, PNG, GIF, WebM)
  - Videos (MP4, WebM, MOV)
  - Title and description
  - Featured content option
- Recent uploads display
- Only accessible to Manager and Admin users

**View Function**: `manager_dashboard(request)`
- Uses `@manager_required` decorator
- Handles file uploads (images and videos)
- Tracks uploader information
- Displays recent uploads by the manager

### Gallery Updates
The gallery system has been enhanced to support both images and videos:

**Model Changes** (`GalleryImage`):
- Added `content_type` field (image/video)
- Added `video` field for video files
- Added `uploaded_by` field to track who uploaded content
- `image` field is now optional (for videos)

**Template Updates** (`gallery.html`):
- Displays both images and videos
- Lightbox supports both media types
- Responsive video player

## Files Involved

1. **Models**: `website/models.py`
   - `UserProfile` model
   - Updated `GalleryImage` model

2. **Views**: `website/views.py`
   - `admin_dashboard()` - Admin dashboard view
   - `manager_dashboard()` - Manager dashboard view

3. **Decorators**: `website/decorators.py`
   - `@admin_required` - Admin access control
   - `@manager_required` - Manager/Admin access control

4. **Templates**:
   - `website/templates/website/admin_dashboard.html`
   - `website/templates/website/manager_dashboard.html`
   - `website/templates/website/gallery.html` (updated)
   - `website/templates/website/base.html` (navigation updated)

5. **URLs**: `website/urls.py`
   - `/admin/dashboard/` - Admin dashboard
   - `/manager/dashboard/` - Manager dashboard

6. **Admin**: `website/admin.py`
   - `UserProfileAdmin` - Admin interface for UserProfile

## Usage

### Setting Up Roles

#### Creating an Admin
The first user created automatically becomes Admin. For existing users:

1. Login as an existing Admin
2. Go to Admin Dashboard: `/admin/dashboard/`
3. Find the user in the table
4. Use the role dropdown to change their role to "Admin"

#### Managing User Roles
**Via Admin Dashboard** (Recommended):
1. Login as Admin
2. Go to `/admin/dashboard/`
3. Find the user in the table
4. Use the role dropdown to select the desired role (User, Manager, or Admin)
5. The role change is applied immediately

**Note**: Admins cannot change their own role for security reasons.

### Manager Content Upload
1. Login as Manager or Admin
2. Navigate to `/manager/dashboard/`
3. Select content type (Image or Video)
4. Upload file
5. Add title and description (optional)
6. Check "Feature this content" if needed
7. Click "Upload Content"

The uploaded content will immediately appear in the gallery section.

## Security Considerations

1. **Access Control**: Decorators ensure only authorized users can access dashboards
2. **File Validation**: File type validation on upload
3. **CSRF Protection**: All forms include CSRF tokens
4. **User Tracking**: All gallery uploads track the uploader
5. **Role Verification**: Multiple checks ensure users have proper roles

## Database Migration

The system includes a migration that:
- Creates `UserProfile` model
- Adds new fields to `GalleryImage` model
- Creates profiles for existing users (if any)

To apply:
```bash
python manage.py migrate
```

## Navigation Integration

The navigation menu automatically shows:
- **Admin** link for Admin users
- **Manager** link for Manager users
- **Logout** link for all authenticated users
- **Login** link for unauthenticated users

## Future Enhancements

Potential improvements:
- Remove Manager role functionality
- User profile pages
- Content moderation features
- Bulk upload functionality
- Content categories/tags
- Analytics dashboard for managers
- Email notifications for role changes

## Notes

- The first user created automatically becomes Admin
- All new users default to "User" role
- Managers can upload both images and videos
- Gallery displays content from all managers
- Admin can see all users but cannot demote themselves
- Role changes are immediate (no approval needed)

