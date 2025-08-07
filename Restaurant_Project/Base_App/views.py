from django.shortcuts import render, get_object_or_404, redirect
from Base_App.models import Items, BookTable, Review, ItemList, Order, OrderItem
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from decimal import Decimal
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from django.core.cache import cache
import json

# Create your views here.
def HomeView(request):
    return render(request, 'Home.html')

def AboutView(request):
    return render(request, 'About.html')

def clear_menu_cache():
    """Clear menu-related cache to refresh categories and items"""
    cache.delete('menu_categories')
    cache.delete('menu_data')

def clear_cache_view(request):
    """Simple view to clear menu cache - useful for debugging"""
    clear_menu_cache()
    return JsonResponse({'status': 'Menu cache cleared successfully'})



def MenuView(request):
    """
    Optimized menu view with caching and database optimization.
    Enhanced for deployment server performance.
    """
    # Try to get categories from cache
    cache_key = 'menu_categories'
    categories = cache.get(cache_key)
    
    if categories is None:
        # Cache miss - fetch from database with optimization
        try:
            # Use select_related and prefetch_related for maximum optimization
            categories = ItemList.objects.select_related().prefetch_related(
                'items__additional_images'
            ).all()
            
            # Debug: Print categories to console
            print(f"Found {categories.count()} categories:")
            for category in categories:
                try:
                    print(f"  - Category ID: {category.id}, Name: {category.Name}")
                    print(f"    Items count: {category.items.count()}")
                    # Debug: Print items in this category
                    for item in category.items.all():
                        try:
                            print(f"      - Item ID: {item.id}, Name: {item.name}, Price: {item.price}")
                        except Exception as e:
                            print(f"      - Error accessing item {item.id}: {str(e)}")
                except Exception as e:
                    print(f"  - Error accessing category {category.id}: {str(e)}")
            
            # Cache for 30 minutes (increased for better performance)
            cache.set(cache_key, categories, 1800)
        except Exception as e:
            print(f"Error loading menu categories: {str(e)}")
            # Fallback to empty categories if there's an error
            categories = []
    else:
        print(f"Using cached categories: {categories.count()} categories found")
    
    context = {
        'categories': categories
    }
    return render(request, 'Menu.html', context)

@csrf_exempt
def get_product_detail(request, pk):
    """
    AJAX endpoint to get product details with multiple images.
    Optimized for deployment server performance.
    """
    try:
        # Check cache first
        cache_key = f'product_detail_{pk}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return JsonResponse(cached_data)
        
        print(f"Processing get_product_detail request for pk: {pk}")
        
        # Use select_related and prefetch_related to optimize database queries
        product = get_object_or_404(
            Items.objects.select_related('Category').prefetch_related('additional_images'), 
            pk=pk
        )
        print(f"Product found: {product.name}")
        
        # Get all images for the product with optimized handling
        images = []
        
        # Add main image if exists
        if product.image:
            try:
                images.append(product.image.url)
            except Exception:
                pass
        
        # Add additional images efficiently
        try:
            additional_images = product.additional_images.all()
            for additional_image in additional_images:
                try:
                    if additional_image.image:
                        images.append(additional_image.image.url)
                except Exception:
                    continue
        except Exception:
            pass
        
        # Build response data with error handling
        try:
            data = {
                'id': product.id,
                'name': str(product.name) if product.name else "Unknown Product",
                'description': str(product.description) if product.description else "",
                'price': int(product.price) if product.price else 0,
                'image_url': product.image.url if product.image else None,
                'images': images,
                'category': str(product.Category.Name) if product.Category and product.Category.Name else "",
            }
        except Exception as e:
            print(f"Error building response data: {str(e)}")
            data = {
                'id': product.id,
                'name': "Unknown Product",
                'description': "",
                'price': 0,
                'image_url': None,
                'images': [],
                'category': "",
            }
        
        # Cache the result for 5 minutes
        cache.set(cache_key, data, 300)
        
        print(f"Returning data for product {data['name']}")
        return JsonResponse(data)
        
    except Exception as e:
        print(f"Error in get_product_detail for pk {pk}: {str(e)}")
        return JsonResponse({'error': 'Product not found or error occurred'}, status=400)

def test_checkout_url(request):
    """
    Test endpoint to verify checkout URL is working.
    """
    return JsonResponse({'status': 'Checkout URL is working'})

@csrf_exempt
def test_server_performance(request):
    """
    Test endpoint to check server performance and response time.
    """
    import time
    start_time = time.time()
    
    # Simulate some database operations
    try:
        # Count total items
        total_items = Items.objects.count()
        # Get first few items
        sample_items = Items.objects.all()[:5]
        
        end_time = time.time()
        response_time = end_time - start_time
        
        return JsonResponse({
            'status': 'Server is responding',
            'response_time': f"{response_time:.3f} seconds",
            'total_items': total_items,
            'sample_items_count': len(sample_items),
            'server_time': time.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return JsonResponse({
            'status': 'Error',
            'error': str(e),
            'server_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def process_checkout(request):
    """
    Process order checkout with comprehensive error handling and email notifications.
    Optimized with caching and batch processing.
    """
    try:
        # Add request rate limiting
        client_ip = request.META.get('REMOTE_ADDR', request.META.get('HTTP_X_FORWARDED_FOR', ''))
        cache_key = f'checkout_attempt_{client_ip}'
        if cache.get(cache_key):
            return JsonResponse({
                'success': False,
                'message': 'Please wait a moment before placing another order.'
            }, status=429)
        cache.set(cache_key, True, 5)  # 5 seconds cooldown
        
        # Set a timeout for the entire operation
        import signal
        from contextlib import contextmanager
        
        @contextmanager
        def timeout(seconds):
            def handler(signum, frame):
                raise TimeoutError("Request timed out")
            
            # Set the timeout handler
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            
            try:
                yield
            finally:
                # Disable the alarm
                signal.alarm(0)
        
        # Execute with timeout
        with timeout(10):  # 10 second timeout
        
        data = json.loads(request.body)
        
        # Extract order data
        customer_name = data.get('customer_name', '').strip()
        customer_email = data.get('customer_email', '').strip()
        customer_phone = data.get('customer_phone', '').strip()
        customer_address = data.get('customer_address', '').strip()
        special_instructions = data.get('special_instructions', '').strip()
        cart_items = data.get('cart_items', [])
        
        # Validation
        if not all([customer_name, customer_email, customer_phone, customer_address]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields.'
            }, status=400)
        
        if not cart_items:
            return JsonResponse({
                'success': False,
                'message': 'Your cart is empty.'
            }, status=400)
        
        # Calculate total amount
        total_amount = Decimal('0.00')
        for item in cart_items:
            price = Decimal(str(item.get('price', 0)))
            quantity = int(item.get('quantity', 1))
            total_amount += price * quantity
        
        # Create order
        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_address=customer_address,
            total_amount=total_amount,
            special_instructions=special_instructions,
            status='pending'
        )
        
        # Create order items
        for item_data in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item_data.get('name', ''),
                product_price=Decimal(str(item_data.get('price', 0))),
                quantity=int(item_data.get('quantity', 1)),
                sugar_level=item_data.get('sugar', ''),
                spoon_preference=item_data.get('spoon', ''),
                extra_demands=item_data.get('extra_demands', '')
            )
        
        # Send confirmation email
        try:
            send_initial_order_email(order)
        except Exception as email_error:
            print(f"Email sending failed: {str(email_error)}")
            # Don't fail the order if email fails
        
        # Clear menu cache to reflect any changes
        clear_menu_cache()
        
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully! Check your email for confirmation.',
            'order_id': order.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        print(f"Error in process_checkout: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while processing your order. Please try again.'
        }, status=500)

def send_initial_order_email(order):
    """
    Send initial order confirmation email to customer asynchronously.
    """
    try:
        context = {
            'customer_name': order.customer_name,
            'order_id': order.id,
            'order_date': order.order_date.strftime('%B %d, %Y at %I:%M %p'),
            'total_amount': order.total_amount,
            'order_items': order.items.all(),
            'special_instructions': order.special_instructions,
            'status': order.get_status_display(),
        }
        
        html_message = render_to_string('emails/order_status_update.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email with fail_silently=True to prevent blocking
        send_mail(
            subject='Order Confirmation - Cafe Coffee',
            message=plain_message,
            from_email=None,
            recipient_list=[order.customer_email],
            html_message=html_message,
            fail_silently=True,
            timeout=5  # 5 second timeout for email sending
        )
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        # Don't raise the exception - let the order complete even if email fails

def BookTableView(request):
    """
    Handle table booking with email confirmation.
    Optimized with caching and rate limiting.
    """
    if request.method == 'POST':
        try:
            # Add request rate limiting
            client_ip = request.META.get('REMOTE_ADDR')
            cache_key = f'booking_attempt_{client_ip}'
            if cache.get(cache_key):
                messages.error(request, 'Please wait a moment before making another booking.')
                return redirect('book')
            cache.set(cache_key, True, 5)  # 5 seconds cooldown
            
            # Extract form data
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            date_str = request.POST.get('date', '').strip()
            guests = int(request.POST.get('guests', 1))
            
            # Validation
            if not all([name, email, phone, date_str]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('book')
            
            if guests < 1 or guests > 20:
                messages.error(request, 'Number of guests must be between 1 and 20.')
                return redirect('book')
            
            # Convert date string to date object
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Create booking record
            booking = BookTable.objects.create(
                name=name,
                email=email,
                phone=phone,
                date=booking_date,
                guests=guests
            )
            
            # Prepare email context
            context = {
                'customer_name': booking.name,
                'customer_email': booking.email,
                'customer_phone': booking.phone,
                'booking_date': booking.date.strftime('%B %d, %Y'),
                'number_of_guests': booking.guests,
            }
            
            # Render HTML and plain text versions of email
            html_message = render_to_string('emails/booking_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                subject='Booking Confirmation - Cafe Coffee',
                message=plain_message,
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                recipient_list=[booking.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Table booked successfully! Check your email for confirmation.')
            return redirect('book')
            
        except Exception as e:
            print(f"Error in booking: {str(e)}")  # For debugging
            messages.error(request, f'Error booking table: {str(e)}')
    
    return render(request, 'Book_Table.html')


def ReviewView(request):
    """
    Optimized review view with caching and pagination.
    """
    # Try to get reviews from cache
    cache_key = 'customer_reviews'
    reviews = cache.get(cache_key)
    
    if reviews is None:
        # Cache miss - fetch from database with optimization
        reviews = Review.objects.all().order_by('-id')[:50]  # Limit to 50 most recent
        
        # Our custom encryption fields handle decryption automatically
        decrypted_reviews = []
        for review in reviews:
            decrypted_review = {
                'id': review.id,
                'username': review.username if review.username else '',
                'description': review.description if review.description else '',
                'rating': int(review.rating) if review.rating else 0,
            }
            decrypted_reviews.append(decrypted_review)
        reviews = decrypted_reviews
        
        # Cache for 15 minutes
        cache.set(cache_key, reviews, 900)
    
    context = {
        'reviews': reviews,
    }
    return render(request, 'Reviews.html', context)

def submit_review(request):
    # Handle POST request to submit a review
    if request.method == 'POST':
        try:
            Review.objects.create(
                username=request.POST['name'],  # Changed from name to username
                description=request.POST['description'],
                rating=int(request.POST['stars'])  # Changed from stars to rating
            )
            # Clear the cache to show new review immediately
            cache.delete('customer_reviews')
            messages.success(request, 'Review submitted successfully!')
            return redirect('review')
        except Exception as e:
            print(f"Error in submit_review: {str(e)}")  # For debugging
            messages.error(request, f'Error submitting review: {str(e)}')
    return redirect('review')