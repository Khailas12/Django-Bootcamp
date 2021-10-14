from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Product


User = get_user_model

class ProductTestCase(TestCase):
    user_a = User(username='bruce', email='bruce3@gmail.com')

