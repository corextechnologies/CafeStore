from django.core.management.base import BaseCommand
from Base_App.models import OrderItem
from decimal import Decimal

class Command(BaseCommand):
    help = 'Fix OrderItem records that have None values for price or quantity'

    def handle(self, *args, **options):
        # Find all OrderItem records with None values
        items_with_none_price = OrderItem.objects.filter(product_price__isnull=True)
        items_with_none_quantity = OrderItem.objects.filter(quantity__isnull=True)
        
        fixed_count = 0
        
        # Fix items with None price
        for item in items_with_none_price:
            item.product_price = Decimal('0.00')
            item.save()
            fixed_count += 1
            self.stdout.write(f"Fixed item {item.id}: set price to 0.00")
        
        # Fix items with None quantity
        for item in items_with_none_quantity:
            item.quantity = 1
            item.save()
            fixed_count += 1
            self.stdout.write(f"Fixed item {item.id}: set quantity to 1")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {fixed_count} OrderItem records')
        ) 