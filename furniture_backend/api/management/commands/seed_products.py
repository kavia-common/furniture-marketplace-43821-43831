from django.core.management.base import BaseCommand
from api.models import Product

# PUBLIC_INTERFACE
class Command(BaseCommand):
    help = 'Seed the database with example products'

    def handle(self, *args, **kwargs):
        sample_products = [
            {
                'name': 'Modern Sofa',
                'price': 749.00,
                'image': 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4',
                'description': 'Sleek blue sofa with wooden legs.',
                'stock': 5
            },
            {
                'name': 'Wooden Dining Set',
                'price': 1199.99,
                'image': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb',
                'description': '6-piece oak dining table with chairs.',
                'stock': 2
            },
            {
                'name': 'Bed Frame',
                'price': 399.50,
                'image': 'https://images.unsplash.com/photo-1499914485622-a88fac53632e',
                'description': 'Queen-sized bed frame in white finish.',
                'stock': 7
            },
        ]

        created = 0
        for pd in sample_products:
            obj, was_created = Product.objects.get_or_create(name=pd['name'], defaults=pd)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created} products'))
