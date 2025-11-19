from django.core.management.base import BaseCommand
from api.models import Product

# PUBLIC_INTERFACE
class Command(BaseCommand):
    help = 'Seed the database with example furniture products (reset first)'

    def handle(self, *args, **kwargs):
        # Wipe existing data (for dev/test idempotency)
        Product.objects.all().delete()

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
            {
                "name": "Minimalist Coffee Table",
                "price": 199.99,
                "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794",
                "description": "A sleek coffee table that fits any living room.",
                "stock": 20,
            },
            {
                "name": "Blue Accent Chair",
                "price": 159.99,
                "image": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2",
                "description": "A pop of color and comfort for your home.",
                "stock": 15,
            },
            {
                "name": "Office Ergonomic Chair",
                "price": 249.99,
                "image": "https://images.unsplash.com/photo-1524758631624-e2822e304c36",
                "description": "Comfort and style for your work from home setup.",
                "stock": 25,
            },
        ]

        for pd in sample_products:
            Product.objects.create(**pd)

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(sample_products)} products (reset performed)'))
