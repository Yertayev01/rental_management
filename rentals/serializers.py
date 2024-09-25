from rest_framework import serializers
from .models import Product, Order, OrderProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'product_id', 'rental_price', 'rental_duration']

class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)
    order_products_data = OrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'start_date', 'end_date', 'total_cost', 'order_products', 'order_products_data']

    def create(self, validated_data):
        order_products_data = validated_data.pop('order_products_data')
        order = Order.objects.create(**validated_data)

        for order_product_data in order_products_data:
            OrderProduct.objects.create(order=order, **order_product_data)

        return order
