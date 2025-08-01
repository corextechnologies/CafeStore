# 🍽️ Coffee Shop Restaurant Website

A modern, responsive restaurant website built with Django featuring an interactive menu, shopping cart functionality, and online ordering system.

## ✨ Features

### 🛒 Shopping Cart System
- **Interactive Cart**: Add items with customizations (sugar level, spoon preference, extra requests)
- **Real-time Updates**: Cart count updates instantly with animations
- **Persistent Storage**: Cart data saved in localStorage
- **Quantity Management**: Increase/decrease quantities or remove items
- **Cart Modal**: Beautiful modal interface for cart management

### 📋 Menu Management
- **Category-based Menu**: Organized by food categories
- **Product Details**: Rich product information with images
- **Customization Options**: Sugar levels, spoon preferences, special requests
- **Responsive Design**: Works perfectly on all devices

### 💳 Checkout System
- **Customer Information**: Collect delivery details
- **Order Summary**: Review items and total before placing order
- **Email Notifications**: Automatic order confirmation emails
- **Order Tracking**: Unique order IDs for tracking

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-first approach
- **Smooth Animations**: Hover effects and transitions
- **Professional Styling**: Coffee-themed color scheme
- **Loading States**: Visual feedback during operations

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)
- Git

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
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver 2550
   ```

9. **Access the website**
   - Main site: http://127.0.0.1:2550/
   - Admin panel: http://127.0.0.1:2550/admin/

## 📁 Project Structure

```
Restaurant_Project/
├── Base_App/                    # Main Django app
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── admin.py                # Admin interface
│   └── migrations/             # Database migrations
├── Restaurant_Project/          # Django project settings
│   ├── settings.py             # Project configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI configuration
├── Template/                   # HTML templates
│   ├── Menu.html              # Menu page with cart
│   ├── Details.html           # Product modal
│   ├── Home.html              # Homepage
│   ├── About.html             # About page
│   ├── Book_Table.html        # Table booking
│   └── Reviews.html           # Customer reviews
├── Static/                     # Static files
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   ├── img/                   # Images
│   └── fonts/                 # Font files
├── Media/                      # User uploaded files
│   └── menu_items/            # Menu item images
├── requirements.txt            # Python dependencies
├── manage.py                  # Django management script
└── README.md                  # This file
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
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Static Files
STATIC_URL=/static/
MEDIA_URL=/media/
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
- **name**: Product name
- **price**: Product price
- **description**: Product description
- **image**: Product image
- **Category**: Foreign key to ItemList

### ItemList (Categories)
- **Name**: Category name
- **items**: Related items

### Order
- **customer_name**: Customer's full name
- **customer_email**: Customer's email
- **customer_phone**: Customer's phone
- **customer_address**: Delivery address
- **special_instructions**: Additional notes
- **total_amount**: Order total
- **order_date**: Order timestamp
- **status**: Order status

### OrderItem
- **order**: Foreign key to Order
- **item_name**: Product name
- **quantity**: Item quantity
- **price**: Item price
- **sugar**: Sugar level
- **spoon**: Spoon preference
- **extra_demands**: Special requests

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
   - View all items
   - Adjust quantities or remove items
   - Click "Proceed to Checkout"

4. **Complete Order**:
   - Fill in customer details
   - Review order summary
   - Click "Place Order"
   - Receive order confirmation

### For Administrators

1. **Access Admin Panel**:
   - Visit http://127.0.0.1:2550/admin/
   - Login with superuser credentials

2. **Manage Menu**:
   - Add/edit categories in "Item Lists"
   - Add/edit menu items in "Items"
   - Upload product images

3. **View Orders**:
   - Check "Orders" section
   - View order details and customer information
   - Update order status

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

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Set up proper database (PostgreSQL recommended)
4. Configure static file serving
5. Set up email backend
6. Use environment variables for sensitive data

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with full control
- **AWS**: Scalable cloud infrastructure
- **Vercel**: Fast static hosting

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

### Debug Mode
Set `DEBUG = True` in settings.py for detailed error messages.

## 📝 API Endpoints

### Menu
- `GET /menu/` - Display menu page
- `GET /get-product/<id>/` - Get product details

### Orders
- `POST /process-checkout/` - Process order checkout
- `POST /submit_review/` - Submit customer review

### Booking
- `POST /book/` - Book table reservation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact: [your-email@example.com]
- Documentation: [link-to-docs]

---

**Built with ❤️ using Django** 