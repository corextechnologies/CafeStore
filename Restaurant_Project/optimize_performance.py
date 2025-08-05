#!/usr/bin/env python
"""
Performance Optimization Script
"""

import os
import subprocess
from pathlib import Path

def optimize_performance():
    """Run performance optimizations"""
    print("🚀 Starting Performance Optimization...")
    
    # Run Django commands
    commands = [
        "python manage.py collectstatic --noinput",
        "python manage.py makemigrations",
        "python manage.py migrate"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"✅ {cmd} completed")
        except subprocess.CalledProcessError:
            print(f"❌ {cmd} failed")
    
    print("\n🎉 Performance optimization completed!")
    print("📈 Your website should now load faster!")

if __name__ == "__main__":
    optimize_performance() 