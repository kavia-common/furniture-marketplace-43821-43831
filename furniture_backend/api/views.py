from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Product, CartItem, Order, OrderItem
from .serializers import (
    ProductSerializer, CartItemSerializer, AddCartItemSerializer,
    OrderSerializer, UserSerializer, LoginSerializer
)

@api_view(['GET'])
def health(request):
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration endpoint."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User login endpoint."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    """Get a list of products."""
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# PUBLIC_INTERFACE
@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, product_id):
    """Get details of a single product."""
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

# PUBLIC_INTERFACE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    """Get the user's cart (items and total)."""
    cart_items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(cart_items, many=True)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return Response({'items': serializer.data, 'total': total})

# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cart_item(request):
    """Add an item to the user's cart."""
    serializer = AddCartItemSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data['product_id']
        qty = serializer.validated_data['quantity']
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        if product.stock < qty:
            return Response({'detail': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        item.quantity = qty
        item.save()
        return Response({'detail': 'Added to cart'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """Create an order from the user's cart."""
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
    total = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total=total)
    for ci in cart_items:
        if ci.product.stock < ci.quantity:
            order.delete()
            return Response({'detail': f"Insufficient stock for {ci.product.name}"}, status=status.HTTP_400_BAD_REQUEST)
        OrderItem.objects.create(
            order=order,
            product=ci.product,
            quantity=ci.quantity,
            price_at_order=ci.product.price
        )
        ci.product.stock -= ci.quantity
        ci.product.save()
    cart_items.delete()
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
