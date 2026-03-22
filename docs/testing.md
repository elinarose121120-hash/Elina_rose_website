# Testing Guide

## Overview
Comprehensive test suite for the Elina Rose website. All tests are located in `website/tests/` directory.

## Test Structure

### Test Files
1. **test_urls.py** - Tests all URL routing and accessibility
2. **test_views.py** - Tests view functionality, context data, and edge cases
3. **test_authentication.py** - Tests authentication and role-based access control
4. **test_dashboards.py** - Tests admin and manager dashboard functionality
5. **test_models.py** - Tests model creation, relationships, and methods

## Running Tests

`SECRET_KEY` must be set (e.g. in `.env` at the project root, or export it for one-off runs). For CI or scripts without `.env`:

```bash
SECRET_KEY=test-only-not-for-production python manage.py test website.tests
```

### Run All Tests
```bash
python manage.py test website.tests
```

### Run Specific Test File
```bash
python manage.py test website.tests.test_urls
python manage.py test website.tests.test_views
python manage.py test website.tests.test_authentication
python manage.py test website.tests.test_dashboards
python manage.py test website.tests.test_models
```

### Run Specific Test Class
```bash
python manage.py test website.tests.test_urls.URLTests
```

### Run Specific Test Method
```bash
python manage.py test website.tests.test_urls.URLTests.test_home_url
```

### Verbose Output
```bash
python manage.py test website.tests -v 2
```

## Test Coverage

### URL Tests (`test_urls.py`)
- Home page accessibility
- About, Gallery, Blog, Contact pages
- Login and Signup pages
- Dashboard access control (admin/manager)
- Blog detail page with valid/invalid posts
- Authentication requirements

### View Tests (`test_views.py`)
- Home view returns published posts
- Home view handles gallery items without images (edge case fix)
- Gallery view returns all items
- Blog view filters published posts
- Contact form submission
- Login with valid/invalid credentials
- Signup with validation (password mismatch, duplicate username)

### Authentication Tests (`test_authentication.py`)
- Regular users cannot access dashboards
- Managers can access manager dashboard
- Managers cannot access admin dashboard
- Admins can access both dashboards
- Superusers can access all dashboards
- Superuser profile auto-creation

### Dashboard Tests (`test_dashboards.py`)
- Admin dashboard displays all users
- Admin can change user roles
- Admin cannot change own role
- Manager can upload images
- Manager can upload videos
- Manager dashboard shows recent uploads

### Model Tests (`test_models.py`)
- UserProfile auto-creation
- First user becomes admin
- Post, GalleryImage, ContactMessage creation
- UserProfile role helper methods

## Important Notes

### Profile Auto-Creation
UserProfile is automatically created when a User is created (via Django signals). In tests, update the existing profile instead of creating a new one:

```python
user = User.objects.create_user(...)
user.profile.role = 'admin'  # Update, don't create
user.profile.save()
```

### Edge Cases Covered
- Gallery items without images (videos only)
- Missing file attributes
- Invalid post IDs
- Duplicate usernames/emails
- Password mismatches
- Unauthenticated access attempts

## Adding New Tests

When adding new features:
1. **Add URL test** - Test the new URL is accessible
2. **Add view test** - Test the view functionality
3. **Add edge case tests** - Test error conditions
4. **Update existing tests** - If feature affects existing functionality

### Test Template
```python
def test_new_feature(self):
    """Test description"""
    # Arrange
    # Act
    # Assert
    self.assertEqual(response.status_code, 200)
```

## Continuous Testing

**IMPORTANT**: Always run tests before committing changes:
```bash
python manage.py test
```

All tests must pass before deploying or merging code.

## Test Maintenance

- Update tests when URLs change
- Update tests when views are modified
- Add tests for bug fixes
- Add tests for new features
- Remove obsolete tests

