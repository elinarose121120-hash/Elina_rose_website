#!/bin/bash

# Quick Start Script for Elina Rose Website

echo "🌹 Setting up Elina Rose Website..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Setup images
echo "Setting up images..."
python setup_images.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000/"
echo ""
echo "To create an admin user, run:"
echo "  python manage.py createsuperuser"
echo ""

