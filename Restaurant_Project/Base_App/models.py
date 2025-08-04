from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField, EncryptedIntegerField, EncryptedEmailField


# Create your models here.

class ItemList(models.Model):
    Name = EncryptedCharField(max_length=20, db_index=True)
    
    def __str__(self):
        return self.Name
    
    class Meta:
        indexes = [
            models.Index(fields=['Name']),
        ]

class Items(models.Model):
    name = EncryptedCharField(max_length=20, db_index=True)
    description = EncryptedTextField(blank=False)
    price = EncryptedIntegerField(db_index=True)
    Category = models.ForeignKey(ItemList, related_name='items', on_delete=models.CASCADE, db_index=True)
    image = models.ImageField(upload_to='menu_items/')

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['Category']),
        ]

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer_name = EncryptedCharField(max_length=100, db_index=True)
    customer_email = EncryptedEmailField(db_index=True)
    customer_phone = EncryptedCharField(max_length=20)
    customer_address = EncryptedTextField()
    order_date = models.DateTimeField(auto_now_add=True, db_index=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', db_index=True)
    special_instructions = EncryptedTextField(blank=True, null=True)
    
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
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, db_index=True)
    product_name = EncryptedCharField(max_length=100, db_index=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    sugar_level = models.CharField(max_length=20)
    spoon_preference = models.CharField(max_length=20)
    extra_demands = EncryptedTextField(blank=True, null=True)
    
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
    name = EncryptedCharField(max_length=50, db_index=True)
    email = EncryptedEmailField(db_index=True)
    phone = EncryptedCharField(max_length=15)
    date = models.DateField(db_index=True)
    guests = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    def __str__(self):
        return f"{self.name} - {self.date}"
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['date']),
        ]

class Review(models.Model):
    username = EncryptedCharField(max_length=50, db_index=True)
    description = EncryptedTextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_index=True
    )

    def __str__(self):
        return f"{self.username} - {self.rating} stars"
    
    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['rating']),
        ]

