# 🔧 Technical Documentation

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Database Schema](#database-schema)
3. [API Documentation](#api-documentation)
4. [Frontend Architecture](#frontend-architecture)
5. [Security Implementation](#security-implementation)
6. [Performance Optimizations](#performance-optimizations)
7. [Testing Strategy](#testing-strategy)
8. [Code Standards](#code-standards)

## 🏗️ Architecture Overview

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django        │    │   Database      │
│   (HTML/CSS/JS) │◄──►│   Backend       │◄──►│   (SQLite/      │
│                 │    │   (Python)      │    │    PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Static Files  │    │   Email Service │    │   File Storage  │
│   (CSS/JS/IMG)  │    │   (SMTP)        │    │   (Media)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **Backend**: Django 5.2.4 (Python 3.10+)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 4
- **Icons**: Font Awesome
- **Email**: SMTP (Gmail)
- **Server**: Gunicorn + Nginx (Production)

## 🗄️ Database Schema

### Models Overview

```python
# Base_App/models.py

class ItemList(models.Model):
    """Menu categories"""
    Name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Items(models.Model):
    """Menu items"""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_items/')
    Category = models.ForeignKey(ItemList, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    """Customer orders"""
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    special_instructions = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

class OrderItem(models.Model):
    """Individual items in orders"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sugar = models.CharField(max_length=10)
    spoon = models.CharField(max_length=20)
    extra_demands = models.TextField(blank=True)
```

### Database Relationships
```
ItemList (1) ──── (Many) Items
Order (1) ──── (Many) OrderItem
```

### Database Indexes
```sql
-- Performance optimization indexes
CREATE INDEX idx_items_category ON Items(Category_id);
CREATE INDEX idx_order_date ON Order(order_date);
CREATE INDEX idx_order_status ON Order(status);
CREATE INDEX idx_orderitem_order ON OrderItem(order_id);
```

## 🌐 API Documentation

### Endpoints

#### Menu Endpoints

**GET /menu/**
- **Description**: Display menu page with categories and items
- **Response**: HTML page with menu data
- **Template**: `Menu.html`

**GET /get-product/{id}/**
- **Description**: Get product details via AJAX
- **Parameters**: `id` (integer) - Product ID
- **Response**: JSON
```json
{
    "name": "Latte",
    "price": "5.99",
    "description": "Smooth espresso with steamed milk",
    "image_url": "/media/menu_items/latte.jpg"
}
```

#### Order Endpoints

**POST /process-checkout/**
- **Description**: Process order checkout
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "+1234567890",
    "customer_address": "123 Main St, City, State",
    "special_instructions": "Extra hot, no ice",
    "cart_items": [
        {
            "name": "Latte",
            "price": 5.99,
            "quantity": 2,
            "sugar": "1",
            "spoon": "plastic",
            "extra_demands": "Extra hot"
        }
    ]
}
```
- **Response**: JSON
```json
{
    "success": true,
    "order_id": 123,
    "message": "Order placed successfully!"
}
```

#### Review Endpoints

**POST /submit_review/**
- **Description**: Submit customer review
- **Parameters**: Form data
- **Response**: JSON success/error message

### Error Responses

```json
{
    "success": false,
    "error": "Error message description"
}
```

## 🎨 Frontend Architecture

### JavaScript Architecture

#### Cart Management
```javascript
// Global cart state
let cart = [];
let currentProduct = null;

// Cart functions
function addToCart(product, customization) {
    // Add item to cart with customizations
}

function updateCartCount() {
    // Update cart count display
}

function updateCartDisplay() {
    // Render cart items in modal
}
```

#### AJAX Communication
```javascript
// Product details fetch
$.ajax({
    url: '/get-product/' + productId + '/',
    method: 'GET',
    success: function(data) {
        // Update modal with product data
    }
});

// Order submission
$.ajax({
    url: '/process-checkout/',
    method: 'POST',
    data: JSON.stringify(orderData),
    contentType: 'application/json',
    success: function(response) {
        // Handle order success
    }
});
```

### CSS Architecture

#### Responsive Design
```css
/* Mobile-first approach */
.single-menu .card-img-top {
    height: 180px; /* Mobile */
}

@media (min-width: 768px) {
    .single-menu .card-img-top {
        height: 200px; /* Tablet */
    }
}

@media (min-width: 992px) {
    .single-menu .card-img-top {
        height: 250px; /* Desktop */
    }
}
```

#### Animation System
```css
/* Cart count animation */
.cart-count {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}
```

## 🔒 Security Implementation

### CSRF Protection
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    # ...
]
```

### Input Validation
```python
# views.py
def process_checkout(request):
    # Validate required fields
    if not all([customer_name, customer_email, customer_phone, customer_address]):
        return JsonResponse({'success': False, 'error': 'Missing required fields'})
    
    # Sanitize inputs
    customer_name = customer_name.strip()
    customer_email = customer_email.lower().strip()
```

### SQL Injection Prevention
- Django ORM automatically prevents SQL injection
- Parameterized queries used throughout
- Input sanitization implemented

### XSS Prevention
```python
# Template auto-escaping
{{ user_input|escape }}  # Manual escaping when needed
```

## ⚡ Performance Optimizations

### Database Optimizations

#### Query Optimization
```python
# Optimized menu query with select_related
def MenuView(request):
    categories = ItemList.objects.select_related().prefetch_related(
        'items__Category'
    ).all()
    return render(request, 'Menu.html', {'categories': categories})
```

#### Caching Implementation
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# views.py
from django.core.cache import cache

def MenuView(request):
    cache_key = 'menu_categories'
    categories = cache.get(cache_key)
    
    if categories is None:
        categories = ItemList.objects.all()
        cache.set(cache_key, categories, 1800)  # Cache for 30 minutes
```

### Frontend Optimizations

#### JavaScript Loading
```html
<!-- Defer non-critical scripts -->
<script src="{% static 'js/vendor/jquery-2.2.4.min.js' %}" defer></script>
<script src="{% static 'js/vendor/bootstrap.min.js' %}" defer></script>
```

#### CSS Optimization
```html
<!-- Critical CSS inline -->
<style>
    /* Critical path CSS here */
    body { font-family: 'Poppins', sans-serif; }
</style>

<!-- Non-critical CSS async -->
<link rel="preload" href="{% static 'css/bootstrap.css' %}" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

#### Image Optimization
```html
<!-- Lazy loading for images -->
<img loading="lazy" src="{% static 'img/logo.png' %}" alt="Logo">
```

## 🧪 Testing Strategy

### Unit Tests
```python
# tests.py
from django.test import TestCase
from django.urls import reverse
from .models import ItemList, Items, Order

class MenuViewTest(TestCase):
    def setUp(self):
        self.category = ItemList.objects.create(Name="Coffee")
        self.item = Items.objects.create(
            name="Latte",
            price=5.99,
            description="Smooth espresso",
            Category=self.category
        )
    
    def test_menu_view(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Latte")
```

### Integration Tests
```python
class CheckoutTest(TestCase):
    def test_checkout_process(self):
        # Test complete checkout flow
        order_data = {
            "customer_name": "Test User",
            "customer_email": "test@example.com",
            "customer_phone": "1234567890",
            "customer_address": "123 Test St",
            "cart_items": []
        }
        
        response = self.client.post(
            reverse('process_checkout'),
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
```

### Frontend Tests
```javascript
// Jest test example
describe('Cart functionality', () => {
    test('addToCart should add item to cart', () => {
        const product = { id: 1, name: 'Latte', price: 5.99 };
        const customization = { sugar: '1', spoon: 'plastic' };
        
        addToCart(product, customization);
        
        expect(cart.length).toBe(1);
        expect(cart[0].name).toBe('Latte');
    });
});
```

## 📏 Code Standards

### Python Standards (PEP 8)
```python
# Good
def calculate_total(items):
    """Calculate total price of items."""
    return sum(item.price * item.quantity for item in items)

# Bad
def calculateTotal(items):
    return sum([item.price*item.quantity for item in items])
```

### JavaScript Standards (ESLint)
```javascript
// Good
const addToCart = (product, customization) => {
    const existingItem = cart.find(item => 
        item.id === product.id && 
        item.sugar === customization.sugar
    );
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: 1,
            sugar: customization.sugar,
            spoon: customization.spoon
        });
    }
};

// Bad
function addToCart(product,customization){
    var existingItem=cart.find(function(item){return item.id==product.id})
    if(existingItem){existingItem.quantity++}else{cart.push({id:product.id,name:product.name})}
}
```

### HTML Standards
```html
<!-- Good -->
<div class="menu-item">
    <img src="{% static 'img/latte.jpg' %}" alt="Latte coffee" loading="lazy">
    <h3>Café Latte</h3>
    <p class="price">$5.99</p>
</div>

<!-- Bad -->
<div class="menu-item"><img src="{% static 'img/latte.jpg' %}"><h3>Café Latte</h3><p class="price">$5.99</p></div>
```

### CSS Standards
```css
/* Good */
.menu-item {
    display: flex;
    flex-direction: column;
    padding: 1rem;
    border-radius: 8px;
    transition: transform 0.3s ease;
}

.menu-item:hover {
    transform: translateY(-2px);
}

/* Bad */
.menu-item{display:flex;flex-direction:column;padding:1rem;border-radius:8px;transition:transform 0.3s ease}.menu-item:hover{transform:translateY(-2px)}
```

## 🔧 Development Tools

### Code Quality Tools
```bash
# Install development dependencies
pip install black flake8 isort

# Format code
black .

# Check code quality
flake8 .

# Sort imports
isort .
```

### Testing Tools
```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Performance Tools
```bash
# Django debug toolbar
pip install django-debug-toolbar

# Database query analysis
python manage.py shell
from django.db import connection
from django.test.utils import override_settings
```

## 📊 Monitoring and Logging

### Logging Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}
```

### Performance Monitoring
```python
# Custom middleware for performance monitoring
import time
from django.utils.deprecation import MiddlewareMixin

class PerformanceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Request-Duration'] = str(duration)
        return response
```

---

**This technical documentation provides a comprehensive overview of the restaurant website's architecture, implementation details, and development standards.** 