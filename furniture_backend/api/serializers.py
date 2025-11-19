from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, CartItem, Order, OrderItem

# PUBLIC_INTERFACE
class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'description', 'stock']

# PUBLIC_INTERFACE
class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem with product details."""
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

# PUBLIC_INTERFACE
class AddCartItemSerializer(serializers.Serializer):
    """Serializer for adding item to cart."""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

# PUBLIC_INTERFACE
class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for an item in the order."""
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price_at_order']

# PUBLIC_INTERFACE
class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order with nested items."""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created', 'total', 'items']

# PUBLIC_INTERFACE
class UserSerializer(serializers.ModelSerializer):
    """Serializer for User sign up."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

# PUBLIC_INTERFACE
class LoginSerializer(serializers.Serializer):
    """Serializer for login inputs."""
    username = serializers.CharField()
    password = serializers.CharField()
