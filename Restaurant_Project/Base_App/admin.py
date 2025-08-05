from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django import forms
from .models import Items, ItemList, Order, OrderItem, BookTable, Review, ItemImage

class OrderItemInline(admin.TabularInline):
    """
    Inline admin for OrderItem to display order items within the Order admin.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'sugar_level', 'spoon_preference', 'extra_demands']
    fields = ['product_name', 'product_price', 'quantity', 'sugar_level',
              'spoon_preference', 'extra_demands']

class ItemImageInline(admin.TabularInline):
    """
    Inline admin for ItemImage to display additional images within the Items admin.
    """
    model = ItemImage
    extra = 1
    fields = ['image', 'caption', 'order']
    ordering = ['order']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order management with status change functionality and email notifications.
    """
    list_display = ['id', 'customer_name', 'customer_email', 'total_amount', 'status', 'order_date']
    list_filter = ['status', 'order_date']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['order_date', 'total_amount']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'customer_address')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'order_date', 'special_instructions')
        }),
        ('Order Status', {
            'fields': ('status',),
            'description': 'Change status to automatically send email notification to customer.'
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to send email notifications when status changes.
        """
        if change:  # Only for existing orders
            try:
                old_obj = Order.objects.get(pk=obj.pk)
                if old_obj.status != obj.status:
                    # Status has changed, send email notification
                    try:
                        self.send_status_change_email(obj, old_obj.status, obj.status)
                        messages.success(request, f'Status changed to "{obj.get_status_display()}". Email notification sent to {obj.customer_email}.')
                    except Exception as e:
                        # Don't fail the save if email fails
                        messages.warning(request, f'Status changed to "{obj.get_status_display()}" but email notification failed: {str(e)}')
            except Exception as e:
                # Don't fail the save if there's any error
                messages.warning(request, f'Status changed but there was an issue: {str(e)}')
        
        super().save_model(request, obj, form, change)
    
    def send_status_change_email(self, order, old_status, new_status):
        """
        Send email notification to customer about status change.
        
        Parameters:
            order: Order object
            old_status: Previous status
            new_status: New status
        """
        status_messages = {
            'pending': {
                'subject': 'Order Confirmed - Cafe Coffee',
                'message': 'Your order has been received and is now being processed.',
                'details': 'We have received your order and our team is preparing it for you.'
            },
            'confirmed': {
                'subject': 'Order Confirmed - Cafe Coffee',
                'message': 'Your order has been confirmed and is in our preparation queue.',
                'details': 'Your order is confirmed and will be prepared shortly.'
            },
            'preparing': {
                'subject': 'Order Being Prepared - Cafe Coffee',
                'message': 'Your order is currently being prepared by our team.',
                'details': 'Our baristas are working on your order right now.'
            },
            'ready': {
                'subject': 'Order Ready for Pickup - Cafe Coffee',
                'message': 'Your order is ready for pickup!',
                'details': 'Your order is ready. Please come to our cafe to collect it.'
            },
            'completed': {
                'subject': 'Order Completed - Cafe Coffee',
                'message': 'Thank you for your order!',
                'details': 'Your order has been completed. We hope you enjoyed your coffee!'
            },
            'cancelled': {
                'subject': 'Order Cancelled - Cafe Coffee',
                'message': 'Your order has been cancelled.',
                'details': 'Your order has been cancelled. Please contact us if you have any questions.'
            }
        }
        
        if new_status in status_messages:
            status_info = status_messages[new_status]
            
            # Prepare email context
            context = {
                'customer_name': order.customer_name,
                'order_id': order.id,
                'order_date': order.order_date.strftime('%B %d, %Y at %I:%M %p'),
                'total_amount': order.total_amount,
                'status': order.get_status_display(),
                'message': status_info['message'],
                'details': status_info['details'],
                'order_items': order.items.all(),
                'special_instructions': order.special_instructions
            }
            
            # Render email template
            html_message = render_to_string('emails/order_status_update.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            try:
                send_mail(
                    subject=status_info['subject'],
                    message=plain_message,
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                    recipient_list=[order.customer_email],
                    html_message=html_message,
                    fail_silently=True,  # Changed to True to prevent hanging
                )
            except Exception as e:
                print(f"Error sending status change email: {str(e)}")
                raise  # Re-raise the exception to be caught by the calling method

# Base_App/admin.py (partial, for ItemsAdmin only)
@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    """
    Admin interface for menu items with custom form to handle price field and multiple images.
    """
    list_display = ['name', 'Category', 'price', 'description', 'image_count']
    list_filter = ['Category']
    search_fields = ['name', 'description']
    inlines = [ItemImageInline]
    
    class ItemsAdminForm(forms.ModelForm):
        price = forms.IntegerField(min_value=0, max_value=1000000)

        class Meta:
            model = Items
            fields = '__all__'

        def clean_price(self):
            price = self.cleaned_data['price']
            if price is None:
                raise forms.ValidationError("Price is required.")
            try:
                price = int(price)
                if price < 0:
                    raise forms.ValidationError("Price cannot be negative.")
            except (ValueError, TypeError):
                raise forms.ValidationError("Price must be a valid integer.")
            return price

    form = ItemsAdminForm
    
    def image_count(self, obj):
        """Display the number of images for this item"""
        count = obj.additional_images.count()
        if obj.image:
            count += 1
        return f"{count} image{'s' if count != 1 else ''}"
    image_count.short_description = 'Images'

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    """
    Admin interface for item images.
    """
    list_display = ['item', 'caption', 'order', 'image_preview']
    list_filter = ['item__Category']
    search_fields = ['item__name', 'caption']
    ordering = ['item', 'order']
    
    def image_preview(self, obj):
        """Show a small preview of the image"""
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 50px;" />'
        return "No image"
    image_preview.short_description = 'Preview'
    image_preview.allow_tags = True

@admin.register(ItemList)
class ItemListAdmin(admin.ModelAdmin):
    """
    Admin interface for menu categories.
    """
    list_display = ['Name']
    search_fields = ['Name']

@admin.register(BookTable)
class BookTableAdmin(admin.ModelAdmin):
    """
    Admin interface for table bookings.
    """
    list_display = ['name', 'email', 'date', 'guests']
    list_filter = ['date']
    search_fields = ['name', 'email']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for customer reviews.
    """
    list_display = ['username', 'rating', 'description']
    list_filter = ['rating']
    search_fields = ['username', 'description']

admin.site.site_header = "Restaurant Admin"
admin.site.index_title = "Welcome to Restaurant Admin"
admin.site.site_title = "Restaurant Admin Portal"