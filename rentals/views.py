# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.db import transaction
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Product, Order, OrderProduct
# from .serializers import ProductSerializer, OrderSerializer, OrderProductSerializer
# from django.db.models import Sum, F, Q
# from datetime import datetime

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Order, OrderProduct
from .serializers import ProductSerializer, OrderSerializer, OrderProductSerializer
from django.db.models import Sum
from datetime import timedelta

# class OrderListView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class ProductListView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class OrderProductDetailView(generics.RetrieveAPIView):
#     serializer_class = OrderProductSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         order_pk = self.kwargs['order_pk']
#         return OrderProduct.objects.filter(order__pk=order_pk)


# class ProductRentalAmountView(generics.ListAPIView):
#     """
#     View to provide rental statistics for each product.
#     """
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['name']
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         start_date = request.query_params.get('start_date')
#         end_date = request.query_params.get('end_date')

#         if start_date and end_date:
#             try:
#                 start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#                 end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
#             except ValueError:
#                 return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

#             product_rentals = OrderProduct.objects.filter(
#                 order__start_date__lte=end_date,
#                 order__end_date__gte=start_date
#             ).values('product__id', 'product__name').annotate(
#                 total_rental_amount=Sum(F('rental_price') * F('rental_duration'))
#             )
#         else:
#             product_rentals = OrderProduct.objects.values('product__id', 'product__name').annotate(
#                 total_rental_amount=Sum(F('rental_price') * F('rental_duration'))
#             )

#         return Response(product_rentals)


# class ProductAvailabilityView(APIView):
#     """
#     View to provide a table of availability intervals when products are not rented.
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         product_id = request.query_params.get('product_id')
#         if not product_id:
#             return Response({"error": "Product ID is required."}, status=400)

#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({"error": "Product not found."}, status=404)

#         # Get all rental periods for the product
#         rentals = OrderProduct.objects.filter(product=product).order_by('order__start_date')

#         # Calculate availability periods between rentals
#         availability_periods = []
#         previous_end = None
#         for rental in rentals:
#             if previous_end and previous_end < rental.order.start_date:
#                 availability_periods.append({
#                     "start_date": previous_end,
#                     "end_date": rental.order.start_date
#                 })
#             previous_end = rental.order.end_date

#         # Add availability from the last rental to infinity
#         if previous_end:
#             availability_periods.append({
#                 "start_date": previous_end,
#                 "end_date": "infinity"
#             })

#         return Response(availability_periods)


# class OrderCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         order_data = request.data.get('order')
#         order_products_data = request.data.get('order_products')

#         order_serializer = OrderSerializer(data=order_data)
#         if order_serializer.is_valid():
#             order = order_serializer.save()
#         else:
#             return Response(order_serializer.errors, status=400)

#         total_cost = 0
#         for product_data in order_products_data:
#             product_data['order'] = order.id
#             order_product_serializer = OrderProductSerializer(data=product_data)
#             if order_product_serializer.is_valid():
#                 order_product = order_product_serializer.save()
#                 total_cost += order_product.rental_price * order_product.rental_duration
#             else:
#                 transaction.set_rollback(True)
#                 return Response(order_product_serializer.errors, status=400)

#         # Update total cost of the order
#         order.total_cost = total_cost
#         order.save()

#         return Response(order_serializer.data, status=201)


# class OrderProductCreateView(APIView):
#     """
#     Endpoint to add a product to an existing order.
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     @transaction.atomic
#     def post(self, request, order_pk):
#         try:
#             order = Order.objects.get(pk=order_pk)
#         except Order.DoesNotExist:
#             return Response({"error": "Order not found."}, status=404)

#         product_data = request.data
#         product_id = product_data.get('product_id')
#         rental_price = product_data.get('rental_price')
#         rental_duration = product_data.get('rental_duration')

#         try:
#             product = Product.objects.get(pk=product_id)
#         except Product.DoesNotExist:
#             return Response({"error": "Product not found."}, status=404)

#         # Ensure that the product is not already in the order
#         if OrderProduct.objects.filter(order=order, product=product).exists():
#             return Response({"error": "This product is already added to the order."}, status=400)

#         # Check for overlapping rentals
#         if OrderProduct.objects.filter(
#             product=product,
#             order__start_date__lt=order.end_date,
#             order__end_date__gt=order.start_date
#         ).exists():
#             return Response({"error": "This product is already rented during the selected time period."}, status=400)

#         # Create an OrderProduct entry
#         order_product_data = {
#             "order": order.id,
#             "product": product.id,
#             "rental_price": rental_price,
#             "rental_duration": rental_duration
#         }

#         order_product_serializer = OrderProductSerializer(data=order_product_data)

#         if order_product_serializer.is_valid():
#             order_product_serializer.save()

#             # Recalculate the order total cost
#             order.total_cost = OrderProduct.objects.filter(order=order).aggregate(
#                 total=Sum(F('rental_price') * F('rental_duration'))
#             )['total'] or 0
#             order.save()

#             return Response(order_product_serializer.data, status=201)
#         else:
#             return Response(order_product_serializer.errors, status=400)
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderProductDetail(generics.RetrieveAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

class RentalSummaryView(APIView):
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        rentals = OrderProduct.objects.filter(
            order__start_date__gte=start_date,
            order__end_date__lte=end_date
        ).values('product__name').annotate(
            total_rental=Sum('rental_cost')
        )
        return Response(rentals)

class ProductAvailabilityView(APIView):
    def get(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        orders = OrderProduct.objects.filter(
            product_id=product_id,
            order__end_date__gte=start_date,
            order__start_date__lte=end_date
        ).order_by('order__start_date')

        availability_periods = []
        current_start = start_date

        for order in orders:
            if order.order.start_date > current_start:
                availability_periods.append((current_start, order.order.start_date))
            current_start = max(current_start, order.order.end_date + timedelta(days=1))

        if current_start <= end_date:
            availability_periods.append((current_start, end_date))

        return Response(availability_periods)