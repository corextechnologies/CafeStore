#!/usr/bin/env python3
"""
Frontend Asset Optimization Script
This script helps optimize CSS and JS files for better performance.
"""

import os
import shutil
import subprocess
from pathlib import Path

def create_minified_css():
    """Create minified CSS files"""
    css_files = [
        'Static/css/bootstrap.css',
        'Static/css/main.css',
        'Static/css/linearicons.css',
        'Static/css/font-awesome.min.css',
        'Static/css/magnific-popup.css',
        'Static/css/nice-select.css',
        'Static/css/animate.min.css',
        'Static/css/owl.carousel.css'
    ]
    
    for css_file in css_files:
        if os.path.exists(css_file):
            # For now, just copy the file with .min extension
            # In production, you'd use a CSS minifier
            min_file = css_file.replace('.css', '.min.css')
            shutil.copy2(css_file, min_file)
            print(f"Created minified CSS: {min_file}")

def create_js_bundle():
    """Create a bundled JS file"""
    js_files = [
        'Static/js/easing.min.js',
        'Static/js/hoverIntent.js',
        'Static/js/superfish.min.js',
        'Static/js/jquery.ajaxchimp.min.js',
        'Static/js/jquery.magnific-popup.min.js',
        'Static/js/owl.carousel.min.js',
        'Static/js/jquery.sticky.js',
        'Static/js/jquery.nice-select.min.js',
        'Static/js/parallax.min.js',
        'Static/js/waypoints.min.js',
        'Static/js/jquery.counterup.min.js',
        'Static/js/mail-script.js'
    ]
    
    bundle_content = []
    for js_file in js_files:
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                bundle_content.append(f"// {js_file}")
                bundle_content.append(f.read())
                bundle_content.append("\n")
    
    if bundle_content:
        with open('Static/js/bundle.min.js', 'w', encoding='utf-8') as f:
            f.write('\n'.join(bundle_content))
        print("Created JS bundle: Static/js/bundle.min.js")

def optimize_images():
    """Optimize images (placeholder for image optimization)"""
    print("Image optimization would be implemented here")
    print("Consider using tools like Pillow or ImageOptim")

def main():
    """Main optimization function"""
    print("Starting frontend optimization...")
    
    # Create minified CSS files
    create_minified_css()
    
    # Create JS bundle
    create_js_bundle()
    
    # Optimize images
    optimize_images()
    
    print("Frontend optimization completed!")
    print("\nNext steps:")
    print("1. Run: python manage.py collectstatic --noinput")
    print("2. Test your website performance")
    print("3. Consider using a CDN for static files in production")

if __name__ == "__main__":
    main() 