# from django.urls import path
# from .views import (
#     OrderListView, OrderDetailView,
#     ProductListView, ProductDetailView,
#     OrderProductDetailView, ProductRentalAmountView, OrderCreateView,
#     OrderProductCreateView, ProductAvailabilityView
# )

# urlpatterns = [
#     path('orders/', OrderListView.as_view(), name='order-list'),
#     path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
#     path('orders/<int:order_pk>/products/', OrderProductCreateView.as_view(), name='order-product-create'),  # Create a new product in an existing order
#     path('orders/<int:order_pk>/products/<int:order_product_pk>/', OrderProductDetailView.as_view(), name='order-product-detail'),
#     path('products/', ProductListView.as_view(), name='product-list'),
#     path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
#     path('products/rental-amount/', ProductRentalAmountView.as_view(), name='product-rental-amount'),
#     path('products/availability/', ProductAvailabilityView.as_view(), name='product-availability'),  # New URL pattern for product availability
#     path('orders/create/', OrderCreateView.as_view(), name='order-create'),
# ]

from django.urls import path
from .views import ProductList, ProductDetail, OrderList, OrderDetail, OrderProductDetail, RentalSummaryView, ProductAvailabilityView

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('orders/', OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
    path('orders/<int:order_pk>/products/<int:order_product_pk>/', OrderProductDetail.as_view(), name='order-product-detail'),
    path('rental-summary/', RentalSummaryView.as_view(), name='rental-summary'),
    path('product-availability/', ProductAvailabilityView.as_view(), name='product-availability'),
]
