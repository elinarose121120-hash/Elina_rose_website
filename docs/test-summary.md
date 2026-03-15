# Test Suite Summary

## Test Coverage

The test suite includes **56 comprehensive tests** covering:

### URL Tests (17 tests)
- All public URLs (home, about, gallery, blog, contact)
- Authentication URLs (login, signup, logout)
- Dashboard URLs with access control
- Blog detail with valid/invalid posts

### View Tests (13 tests)
- Home view with posts and gallery
- Gallery view with all items
- Blog filtering (published only)
- Contact form submission
- Login/signup validation
- Edge cases (gallery items without images)

### Authentication Tests (10 tests)
- Role-based access control
- Superuser access
- Profile auto-creation
- Access restrictions

### Dashboard Tests (8 tests)
- Admin dashboard user management
- Role changes
- Manager content uploads (images/videos)
- Recent uploads display

### Model Tests (8 tests)
- UserProfile auto-creation
- First user becomes admin
- Model creation and relationships
- Role helper methods

## Running Tests

```bash
# Run all tests
python manage.py test website.tests

# Run specific test file
python manage.py test website.tests.test_urls

# Run with verbose output
python manage.py test website.tests -v 2
```

## Test Maintenance Rules

1. **Before committing**: Always run `python manage.py test`
2. **New features**: Add tests immediately
3. **Bug fixes**: Add tests to prevent regression
4. **URL changes**: Update URL tests
5. **View changes**: Update view tests
6. **All tests must pass** before deployment

## Important Test Patterns

### Profile Handling
```python
# Profiles are auto-created, update them:
user.profile.role = 'admin'
user.profile.save()
```

### File Uploads
```python
# Use SimpleUploadedFile for testing
image_file = SimpleUploadedFile("test.jpg", content, content_type="image/jpeg")
```

### Edge Cases
- Gallery items without images/videos
- Missing file attributes
- Invalid IDs
- Unauthenticated access

