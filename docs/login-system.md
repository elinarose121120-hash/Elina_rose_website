# Login System Feature

## Overview
The authentication system provides user registration and login functionality for the Elina Rose website. It allows users to create accounts, sign in, and access protected content or features. The design is intentionally simple and elegant, maintaining the warm, personal aesthetic of the website.

## Implementation

### Authentication Settings
Location: `elina_rose_website/settings.py`

```python
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

- `LOGIN_URL`: Where unauthenticated users are redirected when accessing protected views
- `LOGIN_REDIRECT_URL`: Where users are redirected after successful login
- `LOGOUT_REDIRECT_URL`: Where users are redirected after logout

### URL Configuration
Location: `website/urls.py`

- `/login/` - Login page (handled by `login_view`)
- `/signup/` - User registration page (handled by `signup_view`)
- `/logout/` - Logout functionality (uses Django's built-in `LogoutView`)

### Views
Location: `website/views.py`

#### `login_view(request)`
- Handles both GET and POST requests
- If user is already authenticated, redirects to home
- Authenticates user credentials
- Shows success/error messages
- Supports `next` parameter for redirecting after login

#### `signup_view(request)`
- Handles both GET and POST requests
- If user is already authenticated, redirects to home
- Validates user input (username, email, password, password confirmation)
- Checks for existing username and email
- Creates new user account using Django's `User.objects.create_user()`
- Automatically logs in the user after successful registration
- Shows success/error messages
- Redirects to home page after successful signup

#### Logout
- Uses Django's built-in `LogoutView`
- Automatically handles logout and redirects to home

### Templates
Location: `website/templates/website/`

#### `login.html`
- Clean, elegant login form
- Matches the website's warm aesthetic
- Includes error/success message display
- Link to signup page for new users
- Responsive design
- Styled with inline CSS matching the site's color scheme

#### `signup.html`
- User registration form with username, email, password, and password confirmation
- Matches the login page design aesthetic
- Includes error/success message display
- Link back to login page for existing users
- Client-side password confirmation validation
- Responsive design
- Styled with inline CSS matching the site's color scheme

### Navigation Integration
Location: `website/templates/website/base.html`

The navigation menu dynamically shows:
- **Login** link when user is not authenticated
- **Logout** link when user is authenticated

Uses Django template tags:
```django
{% if user.is_authenticated %}
    <li><a href="{% url 'logout' %}">Logout</a></li>
{% else %}
    <li><a href="{% url 'login' %}">Login</a></li>
{% endif %}
```

## Key Components

### Files Involved
1. `elina_rose_website/settings.py` - Authentication settings
2. `website/urls.py` - URL routing
3. `website/views.py` - Login and signup view logic
4. `website/templates/website/login.html` - Login page template
5. `website/templates/website/signup.html` - Signup/registration page template
6. `website/templates/website/base.html` - Navigation integration

### Dependencies
- Django's built-in authentication system (`django.contrib.auth`)
- Already included in `INSTALLED_APPS` and `MIDDLEWARE`

## Usage

### For Users

#### Signing Up
1. Navigate to `/signup/` or click "Sign up here" link on the login page
2. Enter username, email, password, and confirm password
3. Click "Create Account"
4. Upon successful registration, automatically logged in and redirected to home page

#### Signing In
1. Navigate to `/login/` or click "Login" in the navigation
2. Enter username and password
3. Click "Sign In"
4. Upon successful login, redirected to home page (or the `next` URL if provided)

### For Developers

#### Creating a User
Use Django's management command:
```bash
python manage.py createsuperuser
```

Or create programmatically:
```python
from django.contrib.auth.models import User
user = User.objects.create_user('username', 'email@example.com', 'password')
```

#### Protecting Views
Use the `@login_required` decorator:
```python
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    # Only accessible to logged-in users
    pass
```

#### Checking Authentication in Templates
```django
{% if user.is_authenticated %}
    <!-- Content for logged-in users -->
{% endif %}
```

## Design Considerations

### Aesthetic
- Maintains the warm, elegant color scheme (primary: #d4a574)
- Clean, minimal form design
- Personal, friendly tone ("Welcome Back", "Sign In")
- No corporate or AI-like branding

### User Experience
- Clear error messages for invalid credentials, duplicate usernames/emails, and password mismatches
- Success messages on login and registration
- Password confirmation validation (both client-side and server-side)
- Automatic login after successful registration
- Links between login and signup pages for easy navigation
- Responsive design for mobile devices
- Smooth transitions and hover effects
- Accessible form labels and structure

## Security Notes
- Uses Django's built-in password hashing
- CSRF protection enabled via `{% csrf_token %}`
- Password validation configured in settings
- Session-based authentication
- Secure password requirements enforced

## Future Enhancements
Potential improvements (not yet implemented):
- Password reset functionality
- "Remember me" option
- Social media login integration
- Two-factor authentication
- Email verification for new accounts
- User profile pages

## Notes
- The login system is intentionally simple to maintain the personal website feel
- No complex authentication flows that might feel "corporate"
- Design emphasizes warmth and authenticity over technical complexity
- All styling matches the existing website aesthetic

