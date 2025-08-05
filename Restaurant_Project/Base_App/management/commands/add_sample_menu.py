from django.core.management.base import BaseCommand
from Base_App.models import ItemList, Items


class Command(BaseCommand):
    help = 'Add sample menu categories and items'

    def handle(self, *args, **options):
        # Create categories
        coffee_category, created = ItemList.objects.get_or_create(
            Name="Coffee"
        )
        if created:
            self.stdout.write(f'Created category: {coffee_category.Name}')

        tea_category, created = ItemList.objects.get_or_create(
            Name="Tea"
        )
        if created:
            self.stdout.write(f'Created category: {tea_category.Name}')

        dessert_category, created = ItemList.objects.get_or_create(
            Name="Desserts"
        )
        if created:
            self.stdout.write(f'Created category: {dessert_category.Name}')

        # Create coffee items
        coffee_items = [
            {
                'name': 'Espresso',
                'description': 'Strong Italian coffee served in a small cup',
                'price': 350,
                'Category': coffee_category
            },
            {
                'name': 'Cappuccino',
                'description': 'Espresso with steamed milk and milk foam',
                'price': 450,
                'Category': coffee_category
            },
            {
                'name': 'Latte',
                'description': 'Espresso with steamed milk and a small amount of milk foam',
                'price': 500,
                'Category': coffee_category
            },
            {
                'name': 'Americano',
                'description': 'Espresso with hot water',
                'price': 400,
                'Category': coffee_category
            }
        ]

        # Create tea items
        tea_items = [
            {
                'name': 'Green Tea',
                'description': 'Refreshing green tea with natural antioxidants',
                'price': 250,
                'Category': tea_category
            },
            {
                'name': 'Black Tea',
                'description': 'Classic black tea with rich flavor',
                'price': 200,
                'Category': tea_category
            },
            {
                'name': 'Chai Latte',
                'description': 'Spiced tea with steamed milk',
                'price': 350,
                'Category': tea_category
            }
        ]

        # Create dessert items
        dessert_items = [
            {
                'name': 'Chocolate Cake',
                'description': 'Rich chocolate cake with chocolate frosting',
                'price': 600,
                'Category': dessert_category
            },
            {
                'name': 'Cheesecake',
                'description': 'Creamy New York style cheesecake',
                'price': 550,
                'Category': dessert_category
            },
            {
                'name': 'Tiramisu',
                'description': 'Italian dessert with coffee and mascarpone',
                'price': 650,
                'Category': dessert_category
            }
        ]

        # Add all items
        all_items = coffee_items + tea_items + dessert_items
        
        for item_data in all_items:
            item, created = Items.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'description': item_data['description'],
                    'price': item_data['price'],
                    'Category': item_data['Category']
                }
            )
            if created:
                self.stdout.write(f'Created item: {item.name} - ${item.price}')

        self.stdout.write(
            self.style.SUCCESS('Successfully added sample menu data!')
        ) 