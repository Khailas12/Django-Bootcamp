from typing import Text
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import SET_NULL
from myapp.models import Product
from django.conf import settings


class InventoryWaitList(models.Model):
    product = models.ForeignKey(Product, on_delete=SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField()    
    timestamp = models.DateTimeField(auto_now_add=True)