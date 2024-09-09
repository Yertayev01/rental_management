from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Order, OrderProduct
from .serializers import ProductSerializer, OrderSerializer, OrderProductSerializer
from django.db.models import Sum, F
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderProductDetailView(generics.RetrieveAPIView):
    serializer_class = OrderProductSerializer

    def get_queryset(self):
        order_pk = self.kwargs['order_pk']
        return OrderProduct.objects.filter(order__pk=order_pk)

class ProductRentalAmountView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

            product_rentals = OrderProduct.objects.filter(
                order__start_date__gte=start_date,
                order__end_date__lte=end_date
            ).values('product__id', 'product__name').annotate(
                total_rental_amount=Sum(F('rental_price') * F('rental_duration'))
            )
        else:
            product_rentals = OrderProduct.objects.values('product__id', 'product__name').annotate(
                total_rental_amount=Sum(F('rental_price') * F('rental_duration'))
            )

        return Response(product_rentals)

class OrderCreateView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        order_data = request.data.get('order')
        order_products_data = request.data.get('order_products')

        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()
        else:
            return Response(order_serializer.errors, status=400)

        for product_data in order_products_data:
            product_data['order'] = order.id
            order_product_serializer = OrderProductSerializer(data=product_data)
            if order_product_serializer.is_valid():
                order_product_serializer.save()
            else:
                transaction.set_rollback(True)
                return Response(order_product_serializer.errors, status=400)

        return Response(order_serializer.data, status=201)
