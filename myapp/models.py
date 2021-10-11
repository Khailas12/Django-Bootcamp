from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(null=True, blank=False)
    price = models.IntegerField(default=0)