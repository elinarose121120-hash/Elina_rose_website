# Elina Rose Website

A beautiful, interactive website for Elina Rose built with Django. This website features a modern design that presents Elina as an authentic, engaging personality.

## Features

- **Homepage**: Hero section with engaging introduction and featured content
- **About Page**: Personal story and values
- **Gallery**: Interactive image gallery with lightbox functionality
- **Blog**: Content management for posts and stories
- **Contact**: Contact form for inquiries
- **Responsive Design**: Works beautifully on all devices
- **Interactive Elements**: Smooth animations, parallax effects, and engaging UI

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd Elina_rose
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the website:**
   - Website: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Adding Content

### Adding Images to Gallery

1. Go to the admin panel: http://127.0.0.1:8000/admin/
2. Navigate to "Gallery Images"
3. Click "Add Gallery Image"
4. Upload an image and add a title/description
5. Mark as "Featured" to show on homepage

### Adding Blog Posts

1. Go to the admin panel
2. Navigate to "Posts"
3. Click "Add Post"
4. Fill in the title, content, and optionally upload an image
5. Make sure "Published" is checked to display on the site

### Using Reference Images

You can copy images from the `influencer_reference` folder to the media directory:

```bash
# Create media directories
mkdir -p media/posts media/gallery

# Copy reference images (example)
cp ../influencer_reference/*.jpg media/gallery/
```

Then upload them through the admin panel or use them directly in your posts.

## Project Structure

```
Elina_rose/
├── elina_rose_website/    # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── website/               # Main app
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin configuration
│   └── templates/        # HTML templates
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                # User-uploaded files
├── manage.py
├── requirements.txt
└── README.md
```

## Customization

### Colors

Edit `static/css/style.css` and modify the CSS variables in the `:root` selector:

```css
:root {
    --primary-color: #d4a574;
    --secondary-color: #8b6f47;
    --accent-color: #f5e6d3;
    /* ... */
}
```

### Content

- Update the homepage hero text in `website/templates/website/home.html`
- Modify the about page content in `website/templates/website/about.html`
- Add your social media links in the footer section of `base.html`

## Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in `settings.py`
2. Generate a new `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` with your domain
4. Set up proper database (PostgreSQL recommended)
5. Configure static file serving (WhiteNoise or CDN)
6. Set up SSL/HTTPS
7. Configure email settings for contact form

## License

This project is created for Elina Rose.

## Support

For questions or issues, please contact through the website's contact form.

