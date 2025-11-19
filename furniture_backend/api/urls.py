from django.urls import path
from .views import (
    health,
    register,
    login_view,
    product_list,
    product_detail,
    cart_detail,
    add_cart_item,
    create_order,
)

urlpatterns = [
    path('health/', health, name='Health'),

    # Auth
    path('auth/register/', register, name='register'),
    path('auth/login/', login_view, name='login'),

    # Products
    path('products/', product_list, name='product-list'),
    path('products/<int:product_id>/', product_detail, name='product-detail'),

    # Cart
    path('cart/', cart_detail, name='cart-detail'),
    path('cart/items/', add_cart_item, name='add-cart-item'),

    # Orders
    path('orders/', create_order, name='create-order'),
]
