from django.db import models
from django.contrib.auth import get_user_model
from myapp.models import Product


User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('stale', 'Stale'),
    ('paid', 'Paid'),
    ('shipped', 'Shippied'),
    ('refunded', 'Refunded')
    ) 


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)    # set_null -> if user is deleted, the order will not be deleted
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    shipping_address = models.TextField(blank=False, null=True)
    billing_address = models.TextField(blank=False, null=True)
    timespamp = models.DateTimeField(auto_now_add=True)