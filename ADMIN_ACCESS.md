# Admin Access Information

## Custom Dashboards (Recommended)

**Use these dashboards for all user and content management:**

- **Admin Dashboard**: `http://127.0.0.1:8000/admin/dashboard/`
  - Manage users and roles
  - Change user roles (User/Manager/Admin)
  - View all users

- **Manager Dashboard**: `http://127.0.0.1:8000/manager/dashboard/`
  - Upload images and videos
  - Manage gallery content

## Django Default Admin (Optional - Not Recommended)

The Django default admin panel at `http://127.0.0.1:8000/admin/` is available but **NOT recommended** for regular use.

**To access Django admin:**
1. You need to be logged in as a **superuser** (not just an admin role)
2. Create a superuser: `python manage.py createsuperuser`
3. Login at: `http://127.0.0.1:8000/admin/`

**Note**: The custom dashboards are the primary interface for managing the website. Django admin is only for technical/debugging purposes.

## Important

- **User Management**: Use `/admin/dashboard/` (custom dashboard)
- **Content Management**: Use `/manager/dashboard/` (custom dashboard)
- **Django Admin**: Only for technical purposes, not for regular operations

