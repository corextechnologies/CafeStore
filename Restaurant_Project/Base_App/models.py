from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from .encryption import EncryptedCharField, EncryptedTextField, EncryptedIntegerField, EncryptedEmailField


# Create your models here.

class ItemList(models.Model):
    Name = EncryptedCharField(max_length=500, db_index=True)  # Encrypted - sensitive category data (increased length)
    
    def __str__(self):
        return self.Name
    
    class Meta:
        indexes = [
            models.Index(fields=['Name']),
        ]

class Items(models.Model):
    name = EncryptedCharField(max_length=500, db_index=True)
    description = EncryptedTextField(blank=False)  # Encrypted - sensitive description
    price = EncryptedIntegerField(db_index=True)  # Encrypted - sensitive pricing data
    Category = models.ForeignKey(ItemList, related_name='items', on_delete=models.CASCADE, db_index=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)  # Main image (optional now)
    
    def __str__(self):
        return self.name
    
    @property
    def main_image(self):
        """Get the main image or the first additional image"""
        if self.image:
            return self.image
        first_additional = self.additional_images.first()
        return first_additional.image if first_additional else None
    
    @property
    def all_images(self):
        """Get all images for this item"""
        images = []
        if self.image:
            images.append(self.image)
        images.extend([img.image for img in self.additional_images.all()])
        return images
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['Category']),
        ]

class ItemImage(models.Model):
    """Model for additional images of menu items"""
    item = models.ForeignKey(Items, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_items/additional/')
    caption = models.CharField(max_length=200, blank=True, help_text="Optional caption for the image")
    order = models.PositiveIntegerField(default=0, help_text="Order of display (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['item']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return f"{self.item.name} - Image {self.order}"

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer_name = EncryptedCharField(max_length=1000, db_index=True)  # Encrypted - sensitive customer data (increased length)
    customer_email = EncryptedEmailField(max_length=1000, db_index=True)  # Encrypted - sensitive customer data
    customer_phone = EncryptedCharField(max_length=500)  # Encrypted - sensitive customer data (increased length)
    customer_address = EncryptedTextField()  # Encrypted - sensitive customer data
    order_date = models.DateTimeField(auto_now_add=True, db_index=True)  # Not encrypted - public timestamp
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)  # Not encrypted - needed for calculations
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', db_index=True)  # Not encrypted - needed for processing
    special_instructions = EncryptedTextField(blank=True, null=True)  # Encrypted - sensitive customer data
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} - {self.order_date.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['customer_name']),
            models.Index(fields=['customer_email']),
            models.Index(fields=['order_date']),
            models.Index(fields=['status']),
            models.Index(fields=['total_amount']),
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, db_index=True)  # Not encrypted - foreign key
    product_name = EncryptedCharField(max_length=1000, db_index=True)  # Encrypted - sensitive product data (increased length)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Not encrypted - needed for calculations
    quantity = models.PositiveIntegerField()  # Not encrypted - needed for calculations
    sugar_level = models.CharField(max_length=20)  # Not encrypted - operational data
    spoon_preference = models.CharField(max_length=20)  # Not encrypted - operational data
    extra_demands = EncryptedTextField(blank=True, null=True)  # Encrypted - sensitive customer preferences
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity} - Order #{self.order.id}"
    
    def save(self, *args, **kwargs):
        # Ensure price and quantity are not None
        if self.product_price is None:
            self.product_price = Decimal('0.00')
        if self.quantity is None:
            self.quantity = 1
        super().save(*args, **kwargs)
    
    @property
    def total_price(self):
        if self.product_price is None or self.quantity is None:
            return Decimal('0.00')
        return self.product_price * self.quantity
    
    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product_name']),
        ]

class BookTable(models.Model):
    name = EncryptedCharField(max_length=1000, db_index=True)  # Encrypted - sensitive customer data (increased length)
    email = EncryptedEmailField(max_length=1000, db_index=True)  # Encrypted - sensitive customer data
    phone = EncryptedCharField(max_length=500)  # Encrypted - sensitive customer data (increased length)
    date = models.DateField(db_index=True)  # Not encrypted - public booking date
    guests = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )  # Not encrypted - operational data

    def __str__(self):
        return f"{self.name} - {self.date}"
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['date']),
        ]

class Review(models.Model):
    username = EncryptedCharField(max_length=1000, db_index=True)  # Encrypted - sensitive customer data (increased length)
    description = EncryptedTextField()  # Encrypted - sensitive review content
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_index=True
    )  # Not encrypted - public rating

    def __str__(self):
        return f"{self.username} - {self.rating} stars"
    
    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['rating']),
        ]

