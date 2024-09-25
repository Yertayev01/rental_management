from django.db import models
from django.db.models import Sum, F

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically calculate total cost if not provided
        if self.total_cost is None:
            self.total_cost = OrderProduct.objects.filter(order=self).aggregate(
                total=Sum(F('rental_price') * F('rental_duration'))
            )['total'] or 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} from {self.start_date} to {self.end_date}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_duration = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.product.name} in Order {self.order.id}"
