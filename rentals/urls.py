from django.urls import path
from .views import (
    OrderListView, OrderDetailView,
    ProductListView, ProductDetailView,
    OrderProductDetailView, ProductRentalAmountView, OrderCreateView
)

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_pk>/products/<int:pk>/', OrderProductDetailView.as_view(), name='order-product-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-rental-amount/', ProductRentalAmountView.as_view(), name='product-rental-amount'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
]
