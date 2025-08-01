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
import json

# Create your views here.
def HomeView(request):
    return render(request, 'Home.html')

def AboutView(request):
    return render(request, 'About.html')

#getting all items and item list for menu
from django.core.cache import cache

def MenuView(request):
    """
    Optimized menu view with caching for better performance.
    """
    # Try to get categories from cache
    cache_key = 'menu_categories'
    categories = cache.get(cache_key)
    
    if categories is None:
        # Cache miss - fetch from database with optimization
        categories = ItemList.objects.select_related().prefetch_related(
            'items__Category'
        ).all()
        
        # Cache for 30 minutes
        cache.set(cache_key, categories, 1800)
    
    return render(request, 'Menu.html', {'categories': categories})


def get_product_detail(request, pk):
    try:
        product = get_object_or_404(Items, pk=pk)
        data = {
            'name': product.name,
            'price': str(product.price),  # Convert to string for JSON serialization
            'description': product.description,
            'image_url': product.image.url if product.image else '',
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

def test_checkout_url(request):
    """Simple test view to verify URL routing"""
    return JsonResponse({
        'success': True,
        'message': 'Checkout URL is working correctly!'
    })

@csrf_exempt
@require_http_methods(['POST'])
def process_checkout(request):
    try:
        print("=" * 50)
        print("🔄 CHECKOUT REQUEST RECEIVED")
        print("=" * 50)
        print("📅 Time:", timezone.now())
        print("🌐 Method:", request.method)
        print("📏 Content Length:", len(request.body))
        print("📋 Headers:", dict(request.headers))
        print("📦 Raw Body:", request.body)
        
        data = json.loads(request.body)
        print("✅ Parsed data successfully")
        print("📊 Data keys:", list(data.keys()))
        
        # Extract customer information
        customer_name = data.get('customer_name')
        customer_email = data.get('customer_email')
        customer_phone = data.get('customer_phone')
        customer_address = data.get('customer_address')
        special_instructions = data.get('special_instructions', '')
        cart_items = data.get('cart_items', [])
        
        print("👤 Customer info:", {
            'name': customer_name,
            'email': customer_email,
            'phone': customer_phone,
            'address': customer_address
        })
        print("🛒 Cart items count:", len(cart_items))
        print("📋 Cart items:", cart_items)
        
        # Validate required fields
        if not all([customer_name, customer_email, customer_phone, customer_address]):
            print("❌ Validation failed: missing required fields")
            return JsonResponse({
                'success': False,
                'error': 'All customer information fields are required.'
            }, status=400)
        
        if not cart_items:
            print("❌ Validation failed: empty cart")
            return JsonResponse({
                'success': False,
                'error': 'Cart is empty. Please add items before checkout.'
            }, status=400)
        
        print("✅ Validation passed")
        
        # Calculate total amount
        total_amount = sum(Decimal(item['price']) * Decimal(item['quantity']) for item in cart_items)
        print("💰 Total amount:", total_amount)
        
        # Create order
        print("📝 Creating order...")
        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_address=customer_address,
            total_amount=total_amount,
            special_instructions=special_instructions
        )
        print("✅ Order created with ID:", order.id)
        
        # Send initial "pending" status email (asynchronously to avoid timeout)
        # Temporarily disabled for testing - uncomment when email is configured
        # try:
        #     send_initial_order_email(order)
        # except Exception as e:
        #     print(f"⚠️ Email sending failed but order was created: {str(e)}")
        #     # Continue with order creation even if email fails
        print("📧 Email sending temporarily disabled for testing")
        
        # Create order items
        print("📦 Creating order items...")
        for i, item in enumerate(cart_items):
            order_item = OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                product_price=Decimal(item['price']),
                quantity=int(item['quantity']),
                sugar_level=item['sugar'],
                spoon_preference=item['spoon'],
                extra_demands=item.get('extra_demands', '')
            )
            print(f"✅ Order item {i+1} created:", item['name'])
        
        print("🎉 Order processing completed successfully")
        print("=" * 50)
        
        response_data = {
            'success': True,
            'order_id': order.id,
            'message': f'Order #{order.id} has been placed successfully!'
        }
        
        print("📤 Sending response:", response_data)
        return JsonResponse(response_data)
        
    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", str(e))
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        print("❌ Exception during order processing:", str(e))
        import traceback
        print("📋 Full traceback:")
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'An error occurred while processing your order: {str(e)}'
        }, status=500)

def send_initial_order_email(order):
    """
    Send initial order confirmation email when order is first created.
    
    Parameters:
        order: Order object
    """
    try:
        context = {
            'customer_name': order.customer_name,
            'order_id': order.id,
            'order_date': order.order_date.strftime('%B %d, %Y at %I:%M %p'),
            'total_amount': order.total_amount,
            'status': order.get_status_display(),
            'message': 'Your order has been received and is now being processed.',
            'details': 'We have received your order and our team is preparing it for you.',
            'order_items': order.items.all(),
            'special_instructions': order.special_instructions
        }
        
        # Render email template
        html_message = render_to_string('emails/order_status_update.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email with shorter timeout
        send_mail(
            subject='Order Received - Cafe Coffee',
            message=plain_message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
            recipient_list=[order.customer_email],
            html_message=html_message,
            fail_silently=True,  # Don't raise exception if email fails
        )
        print(f"✅ Initial order email sent to {order.customer_email}")
    except Exception as e:
        print(f"❌ Error sending initial order email: {str(e)}")
        # Don't raise the exception - let the order creation continue

def BookTableView(request):
    """
    Обрабатывает запросы на бронирование столика и отправляет подтверждение по email.
    
    Параметры:
        request: HTTP запрос от пользователя
        
    Возвращает:
        HTTP ответ с результатом бронирования
    """
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            date_str = request.POST['date']
            guests = request.POST['total_person']
            
            # Конвертируем строку даты в объект datetime
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Создаем запись о бронировании
            booking = BookTable.objects.create(
                name=name,
                email=email,
                phone=phone,
                date=booking_date,
                guests=guests
            )
            
            # Подготавливаем данные для email
            context = {
                'customer_name': booking.name,
                'customer_email': booking.email,
                'customer_phone': booking.phone,
                'booking_date': booking.date.strftime('%B %d, %Y'),
                'number_of_guests': booking.guests,
            }
            
            # Рендерим HTML и текстовую версии email
            html_message = render_to_string('emails/booking_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            # Отправляем email
            send_mail(
                subject='Booking Confirmation - Cafe Coffee',
                message=plain_message,
                from_email=None,  # Использует DEFAULT_FROM_EMAIL из settings
                recipient_list=[booking.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Table booked successfully! Check your email for confirmation.')
            return redirect('book')
            
        except Exception as e:
            print(f"Error in booking: {str(e)}")  # Для отладки
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
        reviews = Review.objects.select_related().order_by('-id')[:50]  # Limit to 50 most recent
        
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
            messages.success(request, 'Review submitted successfully!')
            return redirect('review')
        except Exception as e:
            print(str(e))  # For debugging
            messages.error(request, f'Error submitting review: {str(e)}')
    return redirect('review')





