from django.core.management.base import BaseCommand
from django.db import transaction
from Base_App.models import Items, ItemList, Order, OrderItem, BookTable, Review
from Base_App.encryption import decrypt_value, encrypt_value
from django.conf import settings


class Command(BaseCommand):
    help = 'Fix encrypted data issues in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Check and fix Items model
        self.fix_items_data(dry_run)
        
        # Check and fix other models
        self.fix_itemlist_data(dry_run)
        self.fix_order_data(dry_run)
        self.fix_orderitem_data(dry_run)
        self.fix_booktable_data(dry_run)
        self.fix_review_data(dry_run)
        
        self.stdout.write(self.style.SUCCESS('Encrypted data check completed'))

    def fix_items_data(self, dry_run):
        """Fix Items model encrypted data."""
        self.stdout.write('Checking Items model...')
        
        try:
            items = Items.objects.all()
            fixed_count = 0
            
            for item in items:
                needs_fix = False
                
                # Check name field
                if hasattr(item, 'name') and item.name:
                    try:
                        # Try to decrypt to see if it's encrypted
                        decrypted_name = decrypt_value(item.name)
                        # If successful, it was encrypted, so re-encrypt it properly
                        if not dry_run:
                            item.name = encrypt_value(decrypted_name)
                        needs_fix = True
                    except Exception:
                        # Not encrypted, encrypt it
                        if not dry_run:
                            item.name = encrypt_value(item.name)
                        needs_fix = True
                
                # Check description field
                if hasattr(item, 'description') and item.description:
                    try:
                        decrypted_desc = decrypt_value(item.description)
                        if not dry_run:
                            item.description = encrypt_value(decrypted_desc)
                        needs_fix = True
                    except Exception:
                        if not dry_run:
                            item.description = encrypt_value(item.description)
                        needs_fix = True
                
                # Check price field
                if hasattr(item, 'price') and item.price is not None:
                    try:
                        # Try to decrypt to see if it's encrypted
                        decrypted_price = decrypt_value(str(item.price))
                        if not dry_run:
                            item.price = int(decrypted_price)
                        needs_fix = True
                    except Exception:
                        # Not encrypted, encrypt it
                        if not dry_run:
                            item.price = int(item.price)  # Ensure it's an integer
                        needs_fix = True
                
                if needs_fix and not dry_run:
                    item.save()
                    fixed_count += 1
                elif needs_fix and dry_run:
                    fixed_count += 1
            
            if fixed_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Fixed {fixed_count} Items records')
                )
            else:
                self.stdout.write('No Items records need fixing')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fixing Items data: {e}')
            )

    def fix_itemlist_data(self, dry_run):
        """Fix ItemList model encrypted data."""
        self.stdout.write('Checking ItemList model...')
        
        try:
            itemlists = ItemList.objects.all()
            fixed_count = 0
            
            for itemlist in itemlists:
                if hasattr(itemlist, 'Name') and itemlist.Name:
                    try:
                        decrypted_name = decrypt_value(itemlist.Name)
                        if not dry_run:
                            itemlist.Name = encrypt_value(decrypted_name)
                        fixed_count += 1
                    except Exception:
                        if not dry_run:
                            itemlist.Name = encrypt_value(itemlist.Name)
                        fixed_count += 1
            
            if fixed_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Fixed {fixed_count} ItemList records')
                )
            else:
                self.stdout.write('No ItemList records need fixing')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fixing ItemList data: {e}')
            )

    def fix_order_data(self, dry_run):
        """Fix Order model encrypted data."""
        self.stdout.write('Checking Order model...')
        
        try:
            orders = Order.objects.all()
            fixed_count = 0
            
            for order in orders:
                needs_fix = False
                
                # Check encrypted fields
                encrypted_fields = ['customer_name', 'customer_email', 'customer_phone', 
                                  'customer_address', 'special_instructions']
                
                for field_name in encrypted_fields:
                    if hasattr(order, field_name):
                        field_value = getattr(order, field_name)
                        if field_value:
                            try:
                                decrypted_value = decrypt_value(field_value)
                                if not dry_run:
                                    setattr(order, field_name, encrypt_value(decrypted_value))
                                needs_fix = True
                            except Exception:
                                if not dry_run:
                                    setattr(order, field_name, encrypt_value(field_value))
                                needs_fix = True
                
                if needs_fix and not dry_run:
                    order.save()
                    fixed_count += 1
                elif needs_fix and dry_run:
                    fixed_count += 1
            
            if fixed_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Fixed {fixed_count} Order records')
                )
            else:
                self.stdout.write('No Order records need fixing')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fixing Order data: {e}')
            )

    def fix_orderitem_data(self, dry_run):
        """Fix OrderItem model encrypted data."""
        self.stdout.write('Checking OrderItem model...')
        
        try:
            orderitems = OrderItem.objects.all()
            fixed_count = 0
            
            for orderitem in orderitems:
                needs_fix = False
                
                # Check encrypted fields
                if hasattr(orderitem, 'product_name') and orderitem.product_name:
                    try:
                        decrypted_name = decrypt_value(orderitem.product_name)
                        if not dry_run:
                            orderitem.product_name = encrypt_value(decrypted_name)
                        needs_fix = True
                    except Exception:
                        if not dry_run:
                            orderitem.product_name = encrypt_value(orderitem.product_name)
                        needs_fix = True
                
                if hasattr(orderitem, 'extra_demands') and orderitem.extra_demands:
                    try:
                        decrypted_demands = decrypt_value(orderitem.extra_demands)
                        if not dry_run:
                            orderitem.extra_demands = encrypt_value(decrypted_demands)
                        needs_fix = True
                    except Exception:
                        if not dry_run:
                            orderitem.extra_demands = encrypt_value(orderitem.extra_demands)
                        needs_fix = True
                
                if needs_fix and not dry_run:
                    orderitem.save()
                    fixed_count += 1
                elif needs_fix and dry_run:
                    fixed_count += 1
            
            if fixed_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Fixed {fixed_count} OrderItem records')
                )
            else:
                self.stdout.write('No OrderItem records need fixing')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fixing OrderItem data: {e}')
            )

    def fix_booktable_data(self, dry_run):
        """Fix BookTable model encrypted data."""
        self.stdout.write('Checking BookTable model...')
        
        try:
            booktables = BookTable.objects.all()
            fixed_count = 0
            
            for booktable in booktables:
                needs_fix = False
                
                # Check encrypted fields
                encrypted_fields = ['name', 'email', 'phone']
                
                for field_name in encrypted_fields:
                    if hasattr(booktable, field_name):
                        field_value = getattr(booktable, field_name)
                        if field_value:
                            try:
                                decrypted_value = decrypt_value(field_value)
                                if not dry_run:
                                    setattr(booktable, field_name, encrypt_value(decrypted_value))
                                needs_fix = True
                            except Exception:
                                if not dry_run:
                                    setattr(booktable, field_name, encrypt_value(field_value))
                                needs_fix = True
                
                if needs_fix and not dry_run:
                    booktable.save()
                    fixed_count += 1
                elif needs_fix and dry_run:
                    fixed_count += 1
            
            if fixed_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Fixed {fixed_count} BookTable records')
                )
            else:
                self.stdout.write('No BookTable records need fixing')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fixing BookTable data: {e}')
            )

    def fix_review_data(self, dry_run):
        """Fix Review model encrypted data."""
        self.stdout.write('Checking Review model...')
        
        try:
            reviews = Review.objects.all()
            fixed_count = 0
            
            for review in reviews:
                needs_fix = False
                
                # Check encrypted fields
                if hasattr(review, 'username') and review.username:
                    try:
                        decrypted_username = decrypt_value(review.username)
                        if not dry_run:
                            review.username = encrypt_value(decrypted_username)
                        needs_fix = True
                    except Exception:
                        if not dry_run:
                            review.username = encrypt_value(review.username)
                        needs_fix = True
                
                if hasattr(review, 'description') and review.description:
                    try:
                        decrypted_desc = decrypt_value(review.description)
                        if not dry_run:
                            review.description = encrypt_value(decrypted_desc)
                        needs_fix = True
                    except Exception:
                        if not dry_run:
                            review.description = encrypt_value(review.description)
                        needs_fix = True
                
                if needs_fix and not dry_run:
                    review.save()
                    fixed_count += 1
                elif needs_fix and dry_run:
                    fixed_count += 1
            
            if fixed_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Fixed {fixed_count} Review records')
                )
            else:
                self.stdout.write('No Review records need fixing')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fixing Review data: {e}')
            ) 