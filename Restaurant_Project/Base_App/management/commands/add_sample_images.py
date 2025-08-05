from django.core.management.base import BaseCommand
from Base_App.models import Items, ItemImage


class Command(BaseCommand):
    help = 'Add sample additional images to existing menu items'

    def handle(self, *args, **options):
        # Get existing items
        items = Items.objects.all()
        
        if not items.exists():
            self.stdout.write(self.style.WARNING('No items found. Please run add_sample_menu first.'))
            return
        
        # Sample image data (you would replace these with actual image files)
        sample_images = [
            {
                'name': 'Espresso',
                'additional_images': [
                    {'caption': 'Close-up view', 'order': 1},
                    {'caption': 'Side angle', 'order': 2},
                ]
            },
            {
                'name': 'Cappuccino',
                'additional_images': [
                    {'caption': 'Top view with foam', 'order': 1},
                    {'caption': 'Side view', 'order': 2},
                    {'caption': 'With latte art', 'order': 3},
                ]
            },
            {
                'name': 'Chocolate Cake',
                'additional_images': [
                    {'caption': 'Slice view', 'order': 1},
                    {'caption': 'With garnish', 'order': 2},
                ]
            },
            {
                'name': 'Latte',
                'additional_images': [
                    {'caption': 'Steamed milk view', 'order': 1},
                    {'caption': 'With latte art', 'order': 2},
                ]
            },
            {
                'name': 'Tiramisu',
                'additional_images': [
                    {'caption': 'Layered view', 'order': 1},
                    {'caption': 'With coffee sauce', 'order': 2},
                ]
            }
        ]
        
        # Just add to the first few items
        items = Items.objects.all()[:3]  # Get first 3 items
        
        for item in items:
            self.stdout.write(f'Processing {item.name}...')
            
            # Add 2 additional images for each item
            for i in range(1, 3):
                additional_image, created = ItemImage.objects.get_or_create(
                    item=item,
                    caption=f'Additional view {i}',
                    order=i,
                    defaults={
                        'image': item.image  # Use the main image as placeholder
                    }
                )
                if created:
                    self.stdout.write(f'  - Created additional image: Additional view {i}')
                else:
                    self.stdout.write(f'  - Additional image already exists: Additional view {i}')
        
        self.stdout.write(
            self.style.SUCCESS('Sample additional images added! Note: These use the main image as placeholder. Upload actual images via admin.')
        ) 