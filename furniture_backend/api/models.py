from django.db import models
from django.contrib.auth.models import User

# PUBLIC_INTERFACE
class Product(models.Model):
    """A furniture product."""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

# PUBLIC_INTERFACE
class CartItem(models.Model):
    """A single item in a user's cart."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# PUBLIC_INTERFACE
class Order(models.Model):
    """An order placed by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# PUBLIC_INTERFACE
class OrderItem(models.Model):
    """A product entry in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
