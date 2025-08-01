# 🚀 Deployment Guide

This guide covers deploying the Coffee Shop Restaurant Website to various platforms.

## 📋 Pre-Deployment Checklist

### 1. Environment Setup
- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up environment variables
- [ ] Update database settings for production
- [ ] Configure email settings

### 2. Security
- [ ] Generate new `SECRET_KEY`
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS settings
- [ ] Set up proper file permissions

### 3. Performance
- [ ] Enable static file compression
- [ ] Set up caching
- [ ] Optimize database queries
- [ ] Configure CDN (optional)

## 🌐 Deployment Options

### Option 1: Heroku (Recommended for Beginners)

#### Prerequisites
- Heroku account
- Git repository
- Heroku CLI installed

#### Steps

1. **Install Heroku CLI**
   ```bash
   # Windows
   https://devcenter.heroku.com/articles/heroku-cli
   
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-restaurant-app
   ```

4. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
   heroku config:set EMAIL_HOST=smtp.gmail.com
   heroku config:set EMAIL_PORT=587
   heroku config:set EMAIL_USE_TLS=True
   heroku config:set EMAIL_HOST_USER=your-email@gmail.com
   heroku config:set EMAIL_HOST_PASSWORD=your-app-password
   ```

6. **Create Procfile**
   ```bash
   echo "web: gunicorn Restaurant_Project.wsgi --log-file -" > Procfile
   ```

7. **Update requirements.txt**
   ```bash
   # Add these to requirements.txt
   psycopg2-binary==2.9.9
   gunicorn==21.2.0
   whitenoise==6.6.0
   ```

8. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

9. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py collectstatic --noinput
   ```

10. **Create Superuser**
    ```bash
    heroku run python manage.py createsuperuser
    ```

### Option 2: DigitalOcean (VPS)

#### Prerequisites
- DigitalOcean account
- Ubuntu 20.04+ server
- Domain name (optional)

#### Steps

1. **Server Setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3 python3-pip python3-venv nginx -y
   ```

2. **Create Application User**
   ```bash
   sudo adduser restaurant
   sudo usermod -aG sudo restaurant
   ```

3. **Clone Repository**
   ```bash
   cd /home/restaurant
   git clone <your-repo-url> Restaurant_Project
   cd Restaurant_Project
   ```

4. **Set up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure Environment**
   ```bash
   cp env.example .env
   nano .env
   # Edit with your production settings
   ```

6. **Set up Gunicorn**
   ```bash
   sudo nano /etc/systemd/system/restaurant.service
   ```

   Add this content:
   ```ini
   [Unit]
   Description=Restaurant Gunicorn daemon
   After=network.target

   [Service]
   User=restaurant
   Group=www-data
   WorkingDirectory=/home/restaurant/Restaurant_Project
   Environment="PATH=/home/restaurant/Restaurant_Project/venv/bin"
   ExecStart=/home/restaurant/Restaurant_Project/venv/bin/gunicorn --workers 3 --bind unix:/home/restaurant/Restaurant_Project/restaurant.sock Restaurant_Project.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

7. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/restaurant
   ```

   Add this content:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /home/restaurant/Restaurant_Project;
       }

       location /media/ {
           root /home/restaurant/Restaurant_Project;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/home/restaurant/Restaurant_Project/restaurant.sock;
       }
   }
   ```

8. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/restaurant /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

9. **Start Services**
   ```bash
   sudo systemctl start restaurant
   sudo systemctl enable restaurant
   ```

### Option 3: AWS (EC2)

#### Prerequisites
- AWS account
- EC2 instance (Ubuntu recommended)
- Security group configured

#### Steps

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - Select t2.micro (free tier) or larger
   - Configure security group (HTTP:80, HTTPS:443, SSH:22)

2. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Follow DigitalOcean steps** (same as above)

4. **Set up SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

## 🔧 Production Settings

### Update settings.py for Production

```python
import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'restaurant_db'),
        'USER': os.environ.get('DB_USER', 'restaurant_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
```

## 📊 Monitoring and Maintenance

### Logs
```bash
# View application logs
sudo journalctl -u restaurant

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Backup Database
```bash
# PostgreSQL
pg_dump restaurant_db > backup.sql

# SQLite
cp db.sqlite3 backup.sqlite3
```

### Update Application
```bash
cd /home/restaurant/Restaurant_Project
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart restaurant
```

## 🔒 Security Checklist

- [ ] HTTPS enabled
- [ ] Strong SECRET_KEY
- [ ] DEBUG = False
- [ ] Proper ALLOWED_HOSTS
- [ ] Database password protected
- [ ] File permissions set correctly
- [ ] Regular security updates
- [ ] Backup strategy in place

## 📈 Performance Optimization

### Database
- Use PostgreSQL for production
- Set up database indexes
- Optimize queries
- Use connection pooling

### Static Files
- Use CDN (Cloudflare, AWS CloudFront)
- Enable compression
- Set proper cache headers

### Caching
- Redis for session storage
- Memcached for page caching
- Database query caching

## 🆘 Troubleshooting

### Common Issues

1. **500 Error**
   - Check logs: `sudo journalctl -u restaurant`
   - Verify environment variables
   - Check file permissions

2. **Static Files Not Loading**
   - Run: `python manage.py collectstatic`
   - Check STATIC_ROOT path
   - Verify nginx configuration

3. **Database Connection**
   - Check database credentials
   - Verify database is running
   - Test connection manually

4. **Email Not Working**
   - Check SMTP settings
   - Verify app passwords
   - Test with Django shell

### Performance Issues

1. **Slow Loading**
   - Enable caching
   - Optimize images
   - Use CDN
   - Database query optimization

2. **High Memory Usage**
   - Reduce Gunicorn workers
   - Enable memory monitoring
   - Optimize code

## 📞 Support

For deployment issues:
- Check logs first
- Review security settings
- Test locally before deploying
- Use staging environment

---

**Happy Deploying! 🚀** 