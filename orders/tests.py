from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()

class OrderTestCase(TestCase):
    
    def setUp(self):
        user_a = User(username='bruce', email='wahtever')
        user_pswd = 'gotham'
        
        self.user_pswd = user_pswd
        
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_pswd)
        user_a.save()
        
        self.user_a = user_a
        
    # def test_create_order(self):
    #     obj = User.objects.create(user=self.user_a, product=product_a)