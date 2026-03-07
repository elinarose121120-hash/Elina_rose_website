#!/usr/bin/env python
"""
Script to copy reference images to the static/images directory
"""
import os
import shutil
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent
REFERENCE_DIR = BASE_DIR.parent / 'influencer_reference'
STATIC_IMAGES_DIR = BASE_DIR / 'static' / 'images'

# Create static/images directory if it doesn't exist
STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Copy images
if REFERENCE_DIR.exists():
    image_files = list(REFERENCE_DIR.glob('*.jpg'))
    
    if image_files:
        # Copy first image as hero-image.jpg
        if not (STATIC_IMAGES_DIR / 'hero-image.jpg').exists():
            shutil.copy2(image_files[0], STATIC_IMAGES_DIR / 'hero-image.jpg')
            print(f"✓ Copied {image_files[0].name} as hero-image.jpg")
        
        # Copy second image as about-image.jpg if available
        if len(image_files) > 1 and not (STATIC_IMAGES_DIR / 'about-image.jpg').exists():
            shutil.copy2(image_files[1], STATIC_IMAGES_DIR / 'about-image.jpg')
            print(f"✓ Copied {image_files[1].name} as about-image.jpg")
        
        print(f"\n✓ Setup complete! {len(image_files)} reference images found.")
    else:
        print("No .jpg images found in reference directory.")
else:
    print(f"Reference directory not found at {REFERENCE_DIR}")

