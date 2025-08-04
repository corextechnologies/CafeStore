# 🍽️ Coffee Shop Restaurant Website

A modern, responsive restaurant website built with Django featuring an interactive menu, shopping cart functionality, online ordering system, and secure data encryption.

## ✨ Features

### 🛒 Shopping Cart System
- **Interactive Cart**: Add items with customizations (sugar level, spoon preference, extra requests)
- **Real-time Updates**: Cart count updates instantly with smooth animations
- **Persistent Storage**: Cart data saved in localStorage for session persistence
- **Quantity Management**: Increase/decrease quantities or remove items
- **Cart Modal**: Beautiful modal interface for cart management
- **Order Summary**: Detailed order review before checkout

### 📋 Menu Management
- **Category-based Menu**: Organized by food categories with filtering
- **Product Details**: Rich product information with high-quality images
- **Customization Options**: Sugar levels, spoon preferences, special requests
- **Responsive Design**: Works perfectly on all devices (mobile, tablet, desktop)
- **Search & Filter**: Easy navigation through menu items

### 💳 Checkout System
- **Customer Information**: Collect delivery details with validation
- **Order Summary**: Review items and total before placing order
- **Email Notifications**: Automatic order confirmation emails
- **Order Tracking**: Unique order IDs for tracking
- **Status Updates**: Real-time order status tracking

### 🔐 Security Features
- **Data Encryption**: All sensitive data encrypted using django-encrypted-model-fields
- **Secure Forms**: CSRF protection and input validation
- **Environment Variables**: Secure configuration management
- **Database Security**: Encrypted customer information storage

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-first approach with Bootstrap
- **Smooth Animations**: Hover effects and CSS transitions
- **Professional Styling**: Coffee-themed color scheme and typography
- **Loading States**: Visual feedback during operations
- **Accessibility**: WCAG compliant design elements

### 📞 Additional Features
- **Table Booking**: Online table reservation system
- **Customer Reviews**: Rating and review system
- **Admin Panel**: Comprehensive order and menu management
- **Email Integration**: Automated order notifications

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher (tested with Python 3.12.2)
- pip (Python package installer)
- Git
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd Restaurant_Project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv myenv
   
   # Windows
   myenv\Scripts\activate
   
   # Linux/Mac
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env with your settings
   # Update email settings for order notifications
   # Generate a secure SECRET_KEY and FIELD_ENCRYPTION_KEY
   ```

5. **Generate encryption keys**
   ```bash
   # Generate Django secret key
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   
   # Generate field encryption key
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

6. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver 2550
   ```

10. **Access the website**
    - Main site: http://127.0.0.1:2550/
    - Admin panel: http://127.0.0.1:2550/admin/

## 📁 Project Structure

```
Restaurant_Project/
├── Base_App/                    # Main Django app
│   ├── models.py               # Database models with encryption
│   ├── views.py                # View functions and API endpoints
│   ├── admin.py                # Admin interface configuration
│   ├── tests.py                # Unit tests
│   └── migrations/             # Database migrations
├── Restaurant_Project/          # Django project settings
│   ├── settings.py             # Project configuration
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── Template/                   # HTML templates
│   ├── Menu.html              # Menu page with cart functionality
│   ├── Details.html           # Product modal with details
│   ├── Home.html              # Homepage with hero section
│   ├── About.html             # About page
│   ├── Book_Table.html        # Table booking form
│   └── Reviews.html           # Customer reviews and ratings
├── Static/                     # Static files
│   ├── css/                   # Stylesheets and themes
│   ├── js/                    # JavaScript files
│   ├── img/                   # Images and icons
│   └── fonts/                 # Font files
├── Media/                      # User uploaded files
│   └── menu_items/            # Menu item images
├── staticfiles/               # Collected static files
├── requirements.txt            # Python dependencies
├── manage.py                  # Django management script
├── env.example                # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── TECHNICAL_DOCS.md          # Technical documentation
├── DEPLOYMENT.md              # Deployment guide
└── build_optimized_assets.py  # Asset optimization script
```

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Email Settings (for order notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_SUBJECT_PREFIX=[Restaurant]
DEFAULT_FROM_EMAIL=noreply@cafecoffee.com

# Security
FIELD_ENCRYPTION_KEY=your-encryption-key-here
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False

# Performance
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
```

### Email Configuration
For order notifications, configure your email settings:

1. **Gmail Setup**:
   - Enable 2-factor authentication
   - Generate app password
   - Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD

2. **Other Providers**:
   - Update EMAIL_HOST, EMAIL_PORT for your provider
   - Configure appropriate authentication

## 📊 Database Models

### Items
- **name**: Product name (encrypted)
- **price**: Product price (encrypted)
- **description**: Product description (encrypted)
- **image**: Product image
- **Category**: Foreign key to ItemList

### ItemList (Categories)
- **Name**: Category name (encrypted)
- **items**: Related items

### Order
- **customer_name**: Customer's full name (encrypted)
- **customer_email**: Customer's email (encrypted)
- **customer_phone**: Customer's phone (encrypted)
- **customer_address**: Delivery address (encrypted)
- **special_instructions**: Additional notes (encrypted)
- **total_amount**: Order total
- **order_date**: Order timestamp
- **status**: Order status (pending, confirmed, preparing, ready, completed, cancelled)

### OrderItem
- **order**: Foreign key to Order
- **product_name**: Product name (encrypted)
- **product_price**: Item price
- **quantity**: Item quantity
- **sugar_level**: Sugar level preference
- **spoon_preference**: Spoon preference (plastic/metal/none)
- **extra_demands**: Special requests (encrypted)

### BookTable
- **name**: Customer name (encrypted)
- **email**: Customer email (encrypted)
- **phone**: Customer phone (encrypted)
- **date**: Reservation date
- **guests**: Number of guests (1-20)

### Review
- **username**: Customer username (encrypted)
- **description**: Review text (encrypted)
- **rating**: Rating (1-5 stars)

## 🎯 Usage Guide

### For Customers

1. **Browse Menu**:
   - Visit http://127.0.0.1:2550/menu/
   - Browse items by category
   - Click "Order" on any item

2. **Add to Cart**:
   - Select sugar level (0-3 spoons)
   - Choose spoon preference (plastic/metal/none)
   - Add special requests (optional)
   - Click "Add to Order"

3. **Manage Cart**:
   - Click cart icon in header
   - View all items with details
   - Adjust quantities or remove items
   - Click "Proceed to Checkout"

4. **Complete Order**:
   - Fill in customer details
   - Review order summary
   - Click "Place Order"
   - Receive order confirmation email

5. **Book Table**:
   - Visit booking page
   - Select date and number of guests
   - Provide contact information
   - Receive booking confirmation

### For Administrators

1. **Access Admin Panel**:
   - Visit http://127.0.0.1:2550/admin/
   - Login with superuser credentials

2. **Manage Menu**:
   - Add/edit categories in "Item Lists"
   - Add/edit menu items in "Items"
   - Upload product images
   - Set prices and descriptions

3. **View Orders**:
   - Check "Orders" section
   - View order details and customer information
   - Update order status
   - Track order history

4. **Manage Bookings**:
   - View table reservations
   - Update booking status
   - Contact customers if needed

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations Base_App
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic
```

### Database Reset
```bash
python manage.py flush
```

### Code Formatting
```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check code quality with flake8
flake8 .
```

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS` with your domain
3. Set up proper database (PostgreSQL recommended)
4. Configure static file serving with WhiteNoise
5. Set up email backend for production
6. Use environment variables for all sensitive data
7. Enable HTTPS with SSL certificates

### Recommended Hosting Platforms

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn Restaurant_Project.wsgi --log-file -" > Procfile

# Deploy
git push heroku main
```

#### DigitalOcean App Platform
- Connect GitHub repository
- Configure environment variables
- Set build command: `pip install -r requirements.txt`
- Set run command: `gunicorn Restaurant_Project.wsgi`

#### AWS Elastic Beanstalk
- Create EB application
- Configure environment variables
- Deploy using EB CLI

#### Vercel
- Connect repository
- Configure build settings
- Set environment variables

### Environment Variables for Production
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-production-secret-key
FIELD_ENCRYPTION_KEY=your-production-encryption-key
EMAIL_HOST=smtp.yourprovider.com
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   python manage.py runserver 2551
   ```

2. **Database Errors**:
   ```bash
   python manage.py migrate --run-syncdb
   ```

3. **Static Files Not Loading**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Email Not Working**:
   - Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
   - Verify SMTP settings
   - Test with Django shell

5. **Encryption Errors**:
   - Ensure FIELD_ENCRYPTION_KEY is set
   - Check key format (base64 encoded)
   - Regenerate key if needed

### Debug Mode
Set `DEBUG = True` in settings.py for detailed error messages.

## 📝 API Endpoints

### Menu
- `GET /menu/` - Display menu page
- `GET /get-product/<id>/` - Get product details (AJAX)

### Orders
- `POST /process-checkout/` - Process order checkout
- `POST /submit_review/` - Submit customer review

### Booking
- `POST /book/` - Book table reservation

### Cart (JavaScript)
- Cart operations handled client-side with localStorage
- AJAX calls for product details

## 🔒 Security Features

- **Data Encryption**: All sensitive customer data encrypted at rest
- **CSRF Protection**: Built-in Django CSRF protection
- **Input Validation**: Comprehensive form validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Automatic escaping in templates
- **Secure Headers**: Security headers configured

## 📈 Performance Optimization

- **Database Indexing**: Optimized database queries
- **Static File Caching**: Browser caching configured
- **Image Optimization**: Pillow for image processing
- **Code Minification**: Asset optimization script included
- **Caching**: Local memory cache configured

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guide
- Use Black for code formatting
- Write meaningful commit messages
- Add tests for new features
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact: [your-email@example.com]
- Documentation: [link-to-docs]

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap for responsive design components
- Font Awesome for icons
- Contributors and testers

---

**Built with ❤️ using Django 5.2.4 and Python 3.12.2**

*Last updated: December 2024* 