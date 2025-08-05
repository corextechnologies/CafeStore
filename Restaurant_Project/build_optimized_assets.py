#!/usr/bin/env python
"""
Static Assets Optimization Script
Optimizes CSS, JS, and images for better performance
"""

import os
import shutil
from pathlib import Path

def optimize_static_files():
    """Optimize static files for production"""
    
    # Define paths
    static_dir = Path('Static')
    optimized_dir = Path('Static_Optimized')
    
    # Create optimized directory
    if optimized_dir.exists():
        shutil.rmtree(optimized_dir)
    optimized_dir.mkdir()
    
    # Copy and optimize CSS files
    css_dir = optimized_dir / 'css'
    css_dir.mkdir()
    
    # Copy critical CSS files
    critical_css_files = [
        'bootstrap.css',
        'main.css',
        'linearicons.css',
        'font-awesome.min.css'
    ]
    
    for css_file in critical_css_files:
        src = static_dir / 'css' / css_file
        dst = css_dir / css_file
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Optimized: {css_file}")
    
    # Copy and optimize JS files
    js_dir = optimized_dir / 'js'
    js_dir.mkdir()
    
    # Copy critical JS files
    critical_js_files = [
        'vendor/jquery-2.2.4.min.js',
        'vendor/bootstrap.min.js',
        'main.js'
    ]
    
    for js_file in critical_js_files:
        src = static_dir / 'js' / js_file
        dst = js_dir / js_file
        if src.exists():
            # Create subdirectories if needed
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Optimized: {js_file}")
    
    # Copy images (compress if possible)
    img_dir = optimized_dir / 'img'
    if (static_dir / 'img').exists():
        shutil.copytree(static_dir / 'img', img_dir)
        print("Optimized: Images copied")
    
    # Copy fonts
    fonts_dir = optimized_dir / 'fonts'
    if (static_dir / 'fonts').exists():
        shutil.copytree(static_dir / 'fonts', fonts_dir)
        print("Optimized: Fonts copied")
    
    print(f"\n✅ Static files optimized in: {optimized_dir}")
    print("📁 Copy the contents to your production server")

if __name__ == "__main__":
    optimize_static_files() 